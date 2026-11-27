<?php
/* Topic hubs: /worksheets/{country}/{subject}/topics/{topic}/
   One page per topic that collects every skill on that topic, from the lowest grade to the highest.
   Units join a topic when their slug matches 'in' and does not match 'out'.
   Nothing here is stored in the database: the list is built from ws_unit on each request. */

/* Korea (ko): 2022 개정 교육과정. Slugs are English, like Taiwan */
function topic_defs_kr() {
    return array(
        'whole-numbers' => array('name' => '큰 수와 자릿값', 'in' => '/numbers-to|large-numbers|place-value|^(three|four)-digit-numbers$|^counting-to-10$|^comparing-quantities$|^ordinal-numbers$/', 'out' => '/^$/',
            'blurb' => '100까지의 수부터 만, 억, 조까지 자릿값을 알고 수를 읽고 쓰며 크기를 비교합니다.'),
        'addition-and-subtraction' => array('name' => '덧셈과 뺄셈', 'in' => '/add|subtract|putting-together/', 'out' => '/fraction|decimal|integer|polynom/',
            'blurb' => '덧셈과 뺄셈의 뜻부터 받아올림, 받아내림이 있는 세 자리 수의 덧셈과 뺄셈까지 익힙니다.'),
        'multiplication-and-division' => array('name' => '곱셈과 나눗셈', 'in' => '/multipl|divi|order-of|sharing-and-grouping/', 'out' => '/fraction|decimal|integer|polynom/',
            'blurb' => '곱셈구구, 곱셈과 나눗셈의 관계, 세로셈 곱셈, 몫과 나머지가 있는 나눗셈, 혼합 계산을 연습합니다.'),
        'factors-and-multiples' => array('name' => '약수와 배수', 'in' => '/factors|gcf|simplifying/', 'out' => '/^$/',
            'blurb' => '약수와 배수, 최대공약수와 최소공배수를 구하고 이를 이용해 분수를 약분하고 통분합니다.'),
        'fractions-and-decimals' => array('name' => '분수와 소수', 'in' => '/fraction|decimal/', 'out' => '/^$/',
            'blurb' => '분수와 소수의 뜻부터 크기 비교, 덧셈과 뺄셈, 곱셈과 나눗셈까지 차례로 익힙니다.'),
        'estimation' => array('name' => '어림하기', 'in' => '/estimat|round|range-of/', 'out' => '/^$/',
            'blurb' => '몇십, 몇백으로 어림하고, 이상・이하・초과・미만과 올림・버림・반올림으로 수의 범위와 어림값을 나타냅니다.'),
        'shapes' => array('name' => '도형', 'in' => '/lines|angles|rectangles|squares|circles|triangles|quadrilaterals|polygons|shapes|position|congruent|symmetry|cuboids|prisms|cylinders|stacking|polyhedra|circumcenter|similar|pythag|trigonometr|chords/', 'out' => '/^$/',
            'blurb' => '선분과 각, 삼각형과 사각형, 합동과 대칭, 입체도형부터 중학교의 작도, 닮음, 피타고라스 정리, 삼각비, 원의 성질까지 알아봅니다.'),
        'measurement' => array('name' => '측정', 'in' => '/length|time|capacity|weight|mass|perimeter|area|volume|circumference|calendar/', 'out' => '/^$/',
            'blurb' => '길이, 시간, 들이, 무게의 단위부터 둘레와 넓이, 원주와 원의 넓이, 겉넓이와 부피까지 구합니다.'),
        'data' => array('name' => '자료와 가능성', 'in' => '/graph|data|tables|likelihood|chance|averages|sorting|representative|frequenc|counting|probability|variance|box-plots|scatter/', 'out' => '/multiplication-tables|function|coordinates|^counting-to-10$/',
            'blurb' => '자료를 표와 그래프로 나타내고 해석하며, 평균과 가능성부터 중학교의 대푯값, 상대도수, 확률, 분산, 상자그림, 산점도까지 다룹니다.'),
        'ratios-and-proportions' => array('name' => '규칙과 비율', 'in' => '/correspondence|(^|-)ratios?(-|$)|percent|proportion/', 'out' => '/trigonometr/',
            'blurb' => '두 양의 대응 관계를 식으로 나타내고, 비와 비율, 백분율, 비례식과 비례배분을 익힙니다.'),
        'number-systems' => array('name' => '정수, 유리수, 실수', 'in' => '/integer|rational-numbers|prime-factor|repeating-decimal|square-root|irrational|radical/', 'out' => '/^$/',
            'blurb' => '소인수분해, 정수와 유리수의 사칙계산, 순환소수, 제곱근과 무리수, 근호를 포함한 식의 계산까지 중학교의 수 체계를 익힙니다.'),
        'algebra' => array('name' => '문자와 식', 'in' => '/algebraic|exponent|polynomial|factoring/', 'out' => '/^$/',
            'blurb' => '문자를 사용한 식, 일차식의 계산, 지수법칙과 다항식의 계산, 곱셈 공식과 인수분해를 연습합니다.'),
        'equations' => array('name' => '방정식과 부등식', 'in' => '/equation|inequalit/', 'out' => '/function/',
            'blurb' => '일차방정식, 일차부등식, 연립일차방정식, 이차방정식을 풀고 실생활 문제에 활용합니다.'),
        'functions' => array('name' => '함수와 그래프', 'in' => '/coordinates-and-graphs|direct-and-inverse|function/', 'out' => '/^$/',
            'blurb' => '좌표평면과 그래프, 정비례와 반비례, 일차함수와 이차함수의 그래프와 성질을 알아봅니다.'),
        'patterns' => array('name' => '규칙 찾기', 'in' => '/^patterns$|number-patterns/', 'out' => '/^$/',
            'blurb' => '모양과 색, 수의 배열, 덧셈표와 곱셈표, 달력에서 되풀이되거나 일정하게 변하는 규칙을 찾고 나타냅니다.'),
        'coordinate-geometry' => array('name' => '도형의 방정식', 'in' => '/^$/', 'out' => '/^$/',
            'blurb' => '좌표평면에서 두 점 사이의 거리와 내분점, 직선과 원의 방정식, 원과 직선의 위치 관계, 평행이동과 대칭이동을 다룹니다.'),
        'sets-and-logic' => array('name' => '집합과 명제', 'in' => '/^$/', 'out' => '/^$/',
            'blurb' => '집합의 표현과 연산, 명제와 조건, 역과 대우, 충분조건과 필요조건, 절대부등식을 익힙니다.'),
        'exponents-and-logarithms' => array('name' => '지수와 로그', 'in' => '/^$/', 'out' => '/^$/',
            'blurb' => '거듭제곱근과 유리수 지수, 로그와 상용로그, 지수함수와 로그함수의 그래프, 지수·로그방정식과 부등식을 풉니다.'),
        'trigonometry' => array('name' => '삼각함수', 'in' => '/^$/', 'out' => '/^$/',
            'blurb' => '일반각과 호도법, 삼각함수의 값과 그래프, 삼각방정식과 부등식, 사인법칙과 코사인법칙을 익힙니다.'),
        'sequences' => array('name' => '수열', 'in' => '/^$/', 'out' => '/^$/',
            'blurb' => '등차수열과 등비수열의 일반항과 합, ∑의 뜻과 성질, 수열의 귀납적 정의와 수학적 귀납법을 다룹니다.'),
        'calculus' => array('name' => '미분과 적분', 'in' => '/^$/', 'out' => '/^$/',
            'blurb' => '함수의 극한과 연속, 미분계수와 도함수, 접선과 극값, 그래프와 최대·최소, 부정적분과 정적분, 넓이와 거리를 구합니다.'),
        'counting' => array('name' => '경우의 수', 'in' => '/^$/', 'out' => '/^$/',
            'blurb' => '합의 법칙과 곱의 법칙, 순열과 조합, 중복순열과 중복조합, 이항정리로 경우의 수를 셉니다.'),
        'probability-and-statistics' => array('name' => '확률과 통계', 'in' => '/^$/', 'out' => '/^$/',
            'blurb' => '확률의 덧셈정리와 곱셈정리, 조건부확률, 이산확률변수와 이항분포, 정규분포, 표본평균과 통계적 추정을 다룹니다.'),
    );
}

/* Korea, 고등학교: the high-school slugs are listed one by one (most would match the elementary/middle-school patterns wrongly) */
function topic_hs_kr() {
    return array(
        'identities-and-remainder-theorem' => 'algebra', 'complex-numbers' => 'number-systems',
        'discriminant' => 'equations', 'roots-and-coefficients' => 'equations', 'cubic-and-quartic-equations' => 'equations', 'simultaneous-quadratic-equations' => 'equations',
        'linear-inequalities-and-absolute-values' => 'equations', 'quadratic-inequalities' => 'equations',
        'quadratic-equations-and-functions' => 'functions', 'maximum-and-minimum-of-quadratic-functions' => 'functions',
        'functions' => 'functions', 'composite-and-inverse-functions' => 'functions', 'rational-functions' => 'functions', 'irrational-functions' => 'functions',
        'matrices' => '',
        'distance-and-internal-division' => 'coordinate-geometry', 'equations-of-lines' => 'coordinate-geometry', 'distance-from-a-point-to-a-line' => 'coordinate-geometry',
        'equations-of-circles' => 'coordinate-geometry', 'circles-and-lines' => 'coordinate-geometry', 'translations-and-reflections' => 'coordinate-geometry',
        'sets' => 'sets-and-logic', 'set-operations' => 'sets-and-logic', 'propositions-and-conditions' => 'sets-and-logic', 'necessary-and-sufficient-conditions' => 'sets-and-logic', 'absolute-inequalities' => 'sets-and-logic',
        'radicals-and-roots' => 'exponents-and-logarithms', 'exponents' => 'exponents-and-logarithms', 'logarithms' => 'exponents-and-logarithms', 'common-logarithms' => 'exponents-and-logarithms',
        'exponential-and-logarithmic-functions' => 'exponents-and-logarithms', 'exponential-and-logarithmic-equations' => 'exponents-and-logarithms',
        'radians-and-general-angles' => 'trigonometry', 'trigonometric-functions' => 'trigonometry', 'graphs-of-trigonometric-functions' => 'trigonometry', 'law-of-sines-and-cosines' => 'trigonometry',
        'arithmetic-sequences' => 'sequences', 'geometric-sequences' => 'sequences', 'sigma-notation' => 'sequences', 'recursive-sequences-and-induction' => 'sequences',
        'limits-of-functions' => 'calculus', 'continuity' => 'calculus', 'derivatives' => 'calculus', 'rules-of-differentiation' => 'calculus', 'tangent-lines-and-mean-value-theorem' => 'calculus',
        'increasing-decreasing-and-extrema' => 'calculus', 'graphs-and-maximum-minimum' => 'calculus', 'equations-inequalities-and-velocity' => 'calculus', 'indefinite-integrals' => 'calculus',
        'definite-integrals' => 'calculus', 'area-between-curves' => 'calculus', 'velocity-and-distance' => 'calculus',
        'counting-principles' => 'counting', 'permutations' => 'counting', 'combinations' => 'counting', 'permutations-with-repetition' => 'counting', 'combinations-with-repetition' => 'counting', 'binomial-theorem' => 'counting',
        'probability-and-addition-rule' => 'probability-and-statistics', 'conditional-probability' => 'probability-and-statistics', 'independence-and-multiplication-rule' => 'probability-and-statistics',
        'discrete-random-variables' => 'probability-and-statistics', 'binomial-distribution' => 'probability-and-statistics', 'normal-distribution' => 'probability-and-statistics', 'sampling-and-estimation' => 'probability-and-statistics',
    );
}

/* topic_defs_kr() + the high-school list: each high-school slug goes only to its listed topic */
function topic_defs_kr_all() {
    $t = topic_defs_kr();
    $hs = topic_hs_kr();
    foreach ($t as $k => $d) {
        $mine = array();
        $other = array();
        foreach ($hs as $slug => $tk) {
            if ($tk === $k) $mine[] = preg_quote($slug, '/');
            else $other[] = preg_quote($slug, '/');
        }
        $in = substr($d['in'], 1, -1);
        $out = substr($d['out'], 1, -1);
        if ($mine) $in = '(?:' . $in . ')|^(?:' . implode('|', $mine) . ')$';
        if ($other) $out = '(?:' . $out . ')|^(?:' . implode('|', $other) . ')$';
        $t[$k]['in'] = '/' . $in . '/';
        $t[$k]['out'] = '/' . $out . '/';
    }
    return $t;
}

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

/* China (cn): simplified Chinese topic names and cn unit slugs */
function topic_defs_cn() {
    return array(
        'numbers' => array('name' => '数的认识', 'in' => '/^numbers|large-numbers|composing-numbers|negative-numbers|factors-and-multiples|^counting-to|counting-in-groups|comparing-quantities|ordinal-numbers|splitting-and-combining/', 'out' => '/^$/',
            'blurb' => '从 10 以内的数、100 以内的数到亿以上的数，认识数位和计数单位、数的组成、比大小，因数与倍数，以及负数。'),
        'addition-and-subtraction' => array('name' => '加法和减法', 'in' => '/add|subtract|carrying|borrowing|number-sentences/', 'out' => '/fraction|decimal|rational/',
            'blurb' => '从 10 以内的加减法、20 以内的进位加法和退位减法，到 100 以内和万以内的笔算加减。'),
        'multiplication' => array('name' => '乘法', 'in' => '/multipl|meaning-of-times|three-digit-by-two/', 'out' => '/fraction|decimal|factors|rational|polynomial|formulas/',
            'blurb' => '乘法的意义、乘法口诀、倍的认识，以及多位数乘一位数、两位数乘两位数和三位数乘两位数。'),
        'division' => array('name' => '除法', 'in' => '/divi/', 'out' => '/fraction|decimal|rational/',
            'blurb' => '平均分和除法的意义、用乘法口诀求商、有余数的除法，以及除数是一位数和两位数的除法。'),
        'order-of-operations' => array('name' => '四则运算和运算律', 'in' => '/order-of-operations|laws-of-operations|mixed-operations/', 'out' => '/^$/',
            'blurb' => '混合运算的顺序、小括号，以及加法和乘法的交换律、结合律和乘法分配律。'),
        'word-problems' => array('name' => '解决问题', 'in' => '/two-step|chickens-and-rabbits|pigeonhole/', 'out' => '/^$/',
            'blurb' => '两步计算的实际问题，以及鸡兔同笼、鸽巢问题等数学广角的问题。'),
        'estimation' => array('name' => '估算和近似数', 'in' => '/estimat|rounding/', 'out' => '/^$/',
            'blurb' => '加减法和乘除法的估算，用“四舍五入”法求近似数，用“万”“亿”作单位。'),
        'fractions' => array('name' => '分数', 'in' => '/fraction/', 'out' => '/algebraic/',
            'blurb' => '分数的初步认识、分数的意义和性质、约分和通分，以及分数的加减乘除。'),
        'decimals' => array('name' => '小数', 'in' => '/decimal/', 'out' => '/^$/',
            'blurb' => '小数的初步认识、小数的意义和性质，以及小数的加减法、乘法和除法。'),
        'ratios-and-percentages' => array('name' => '比、比例和百分数', 'in' => '/(^|-)ratios?(-|$)|^proportion$|percent|discounts/', 'out' => '/^$/',
            'blurb' => '比的意义和化简、按比分配，百分数，折扣、成数、税率和利率，以及正比例、反比例和比例尺。'),
        'rational-and-real-numbers' => array('name' => '有理数与实数', 'in' => '/rational-numbers|real-numbers|powers-and-scientific|quadratic-radicals/', 'out' => '/^$/',
            'blurb' => '正数和负数、数轴、相反数和绝对值，有理数的加减乘除和乘方，科学记数法，平方根、立方根、实数和二次根式。'),
        'algebra' => array('name' => '整式与分式', 'in' => '/algebraic|polynomials|multiplication-formulas|factorization/', 'out' => '/^$/',
            'blurb' => '用字母表示数，整式的加减，幂的运算和整式的乘法，乘法公式，因式分解，以及分式的运算。'),
        'equations-and-inequalities' => array('name' => '方程与不等式', 'in' => '/equation|inequalit/', 'out' => '/of-circles/',
            'blurb' => '简易方程、一元一次方程、二元一次方程组、不等式与不等式组、分式方程和一元二次方程。'),
        'functions' => array('name' => '函数', 'in' => '/coordinate-plane|functions$|exponents-and-logarithms/', 'out' => '/trigonometric/',
            'blurb' => '平面直角坐标系，一次函数、二次函数和反比例函数，函数的概念与性质，指数、对数和指数函数、对数函数。'),
        'measurement' => array('name' => '常见的量', 'in' => '/centimeters|comparing-length|(^|-)grams|measurement-units|hectares|^rmb$|telling-time|hours|years-months/', 'out' => '/^$/',
            'blurb' => '认识人民币，厘米和米、克和千克、吨和千米，时、分、秒和年、月、日，以及公顷和平方千米。'),
        'area-and-perimeter' => array('name' => '周长和面积', 'in' => '/^area|rectangles-and-squares|^circles$/', 'out' => '/^$/',
            'blurb' => '长方形和正方形的周长，面积单位，长方形、平行四边形、三角形、梯形的面积，以及圆的周长和面积。'),
        'shapes' => array('name' => '平面图形', 'in' => '/2d-shapes|recognizing-shapes|^angles$|measuring-angles|parallel-perpendicular|^triangles$|rectangles-and-squares|^circles$/', 'out' => '/^$/',
            'blurb' => '认识图形、角的初步认识和角的度量，平行与垂直，三角形、四边形和圆的特征。'),
        'geometry' => array('name' => '三角形、四边形与圆', 'in' => '/geometric-figures|intersecting|triangles-and-polygons|congruent|parallelograms$|pythagorean|similarity|^trigonometric-functions$|circle-geometry/', 'out' => '/^$/',
            'blurb' => '直线、射线、线段和角，相交线与平行线，三角形和多边形，全等和相似，勾股定理，平行四边形，锐角三角函数，以及圆。'),
        'solids' => array('name' => '立体图形', 'in' => '/3d-shapes|observing|cuboids|cylinders|projections|solid-geometry/', 'out' => '/^$/',
            'blurb' => '认识长方体、正方体、圆柱和球，观察物体，长方体、正方体、圆柱和圆锥的表面积和体积，投影与视图，以及高中的立体几何初步。'),
        'position-and-movement' => array('name' => '图形的位置与运动', 'in' => '/position|directions|symmetry|rotation/', 'out' => '/^$/',
            'blurb' => '上下前后左右、东南西北，用数对和方向与距离确定位置，以及轴对称、平移和旋转。'),
        'statistics' => array('name' => '统计与概率', 'in' => '/sorting|data-collection|data-analysis|^tables$|graphs|charts|likelihood|^probability$|^statistics$|paired-data/', 'out' => '/trigonometric/',
            'blurb' => '分类与整理、统计表和统计图、平均数、可能性，频数分布直方图、中位数、众数、方差、概率，以及高中的抽样、百分位数和成对数据的统计分析。'),
        'sets-and-logic' => array('name' => '集合、逻辑与不等式', 'in' => '/^sets$|^logic$|quadratic-inequalities/', 'out' => '/^$/',
            'blurb' => '高中数学的预备知识：集合的运算、充要条件、全称量词与存在量词、基本不等式和一元二次不等式。'),
        'trigonometry' => array('name' => '三角函数', 'in' => '/angles-and-trigonometric|trigonometric-identities|graphs-of-trigonometric|solving-triangles/', 'out' => '/^$/',
            'blurb' => '任意角和弧度制、三角函数的定义和诱导公式、三角恒等变换、y ＝ A sin(ωx ＋ φ) 的图象与性质，以及正弦定理和余弦定理。'),
        'vectors-and-complex-numbers' => array('name' => '向量与复数', 'in' => '/vectors|complex-numbers/', 'out' => '/^$/',
            'blurb' => '平面向量和空间向量的坐标运算、数量积、夹角和法向量，以及复数的四则运算和复平面。'),
        'analytic-geometry' => array('name' => '解析几何', 'in' => '/^lines$|equations-of-circles|ellipses|hyperbolas|parabolas/', 'out' => '/^$/',
            'blurb' => '直线的方程、圆的方程，以及椭圆、双曲线、抛物线的标准方程和几何性质。'),
        'sequences-and-derivatives' => array('name' => '数列与导数', 'in' => '/^sequences$|derivatives/', 'out' => '/^$/',
            'blurb' => '等差数列和等比数列，导数的概念和运算，用导数研究函数的单调性、极值和最值。'),
        'counting-and-probability' => array('name' => '计数原理与概率分布', 'in' => '/counting-principles|binomial-theorem|random-variables|conditional-probability/', 'out' => '/^$/',
            'blurb' => '分类加法和分步乘法计数原理、排列组合、二项式定理、随机变量的分布列、二项分布、超几何分布、条件概率和正态分布。'),
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

/* Switzerland (ch, Deutschschweiz): the German topics and slugs, written the Swiss way (ss, Franken und Rappen) */
function topic_defs_ch() {
    $d = topic_defs_de();
    $m = array('ß' => 'ss', 'Euro und Cent' => 'Franken und Rappen', 'Kommaschreibweise' => 'Dezimalschreibweise');
    foreach ($d as $k => $v) {
        $d[$k]['name'] = strtr($v['name'], $m);
        $d[$k]['blurb'] = strtr($v['blurb'], $m);
    }
    // Kindergarten slugs
    $kg = array('zahlen-und-stellenwerte' => '^zaehlen-bis|mengen-vergleichen', 'plus-und-minus' => 'dazuzaehlen|wegnehmen|zahlen-zerlegen',
                'groessen' => 'tagesablauf', 'daten-und-zufall' => 'sortieren-und');
    foreach ($kg as $k => $re) {
        $d[$k]['in'] = preg_replace('#/$#', '|' . $re . '/', $d[$k]['in']);
    }
    // Gymnasium slugs
    $gym = array('exponential-potenz-und-winkelfunktionen' => 'gebrochenrational', 'muster-und-strukturen' => 'folgen|reihen-und',
                 'daten-und-zufall' => 'binomial|statistische');
    foreach ($gym as $k => $re) {
        $d[$k]['in'] = preg_replace('#/$#', '|' . $re . '/', $d[$k]['in']);
    }
    $gout = 'gebrochenrational|stammfunktion|integral|ableitung|kurvendiskussion|extremwert|vektor|skalarprodukt|geraden-und-ebenen';
    foreach (array('zahlen-und-stellenwerte', 'lineare-funktionen-und-gleichungssysteme', 'geometrie') as $k) {
        $d[$k]['out'] = $d[$k]['out'] === '/^$/' ? '/' . $gout . '/' : preg_replace('#/$#', '|' . $gout . '/', $d[$k]['out']);
    }
    $d['differenzial-und-integralrechnung'] = array('name' => 'Differenzial- und Integralrechnung',
        'in' => '/ableitung|kurvendiskussion|extremwert|stammfunktion|integral/', 'out' => '/^$/',
        'blurb' => 'Ableitungen und Tangenten, Ableitungsregeln, Kurvendiskussion, Extremwertaufgaben, Stammfunktionen, bestimmte Integrale und Flächen.');
    $d['vektorgeometrie'] = array('name' => 'Vektorgeometrie',
        'in' => '/vektor|skalarprodukt|geraden-und-ebenen/', 'out' => '/^$/',
        'blurb' => 'Vektoren in der Ebene und im Raum, Betrag, Skalar- und Vektorprodukt, Winkel, Geraden und Ebenen, Schnittpunkte und Abstände.');
    return $d;
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
            'in' => '/numeri|ordinare|potenz|pari-e-dispari|espression|multipli|mcd|insiemi|radice|radical/', 'out' => '/decimal|frazion/',
            'blurb' => 'Leggere, scrivere e scomporre i numeri, il valore posizionale delle cifre, confrontare e ordinare i numeri sulla retta.'),
        'addizione-e-sottrazione' => array('name' => 'Addizione e sottrazione',
            'in' => '/addizion|sottrazion|calcolo-mentale|amici-del/', 'out' => '/^$/',
            'blurb' => 'Calcolo mentale, addizioni e sottrazioni in colonna con il cambio, prova e proprietà delle operazioni.'),
        'moltiplicazione-e-divisione' => array('name' => 'Moltiplicazione e divisione',
            'in' => '/moltiplic|division|tabellin|doppio/', 'out' => '/polinom/',
            'blurb' => 'Tabelline, moltiplicazioni in colonna, divisioni con il resto, moltiplicare e dividere per 10, 100 e 1000.'),
        'frazioni-e-decimali' => array('name' => 'Frazioni e numeri decimali',
            'in' => '/frazion|decimal|percentual/', 'out' => '/algebric/',
            'blurb' => 'Unità frazionarie, frazione di una quantità, frazioni decimali, numeri decimali con l’euro e le misure, percentuali.'),
        'problemi' => array('name' => 'Problemi',
            'in' => '/problemi|compravendita/', 'out' => '/^$/',
            'blurb' => 'Problemi con una o due operazioni, dati utili e inutili, domande nascoste, problemi con l’euro e le misure.'),
        'misure' => array('name' => 'Misure',
            'in' => '/misure|lunghezz|peso|capacit|euro|orologio|tempo/', 'out' => '/circonferenz/',
            'blurb' => 'Misure di lunghezza, peso e capacità, equivalenze, l’euro, l’orologio e la durata del tempo.'),
        'geometria' => array('name' => 'Geometria',
            'in' => '/linee|angoli|figure|poligon|perimetro|solidi|simmetria|percorsi|cerchio|circonferenz|trasformazion|cartesian|triangol|quadrilater|isometri|segmenti|rette|pitagora|similitudine|poliedri|rotazione|parallelogramm|trapez|spazio|(^|-)area(-|$)/', 'out' => '/^$/',
            'blurb' => 'Linee e angoli, poligoni e perimetro, figure solide, simmetria, percorsi e reticoli.'),
        'proporzioni-e-funzioni' => array('name' => 'Proporzioni e funzioni',
            'in' => '/rapporti|proporzional|(^|-)retta(-|$)|funzion|successioni/', 'out' => '/esponenzial|logaritm|goniometr|studio-di-funzione|dominio-e-segno/',
            'blurb' => 'Rapporti e proporzioni, grandezze direttamente e inversamente proporzionali, funzioni e rette nel piano cartesiano.'),
        'geometria-analitica' => array('name' => 'Geometria analitica e coniche',
            'in' => '/cartesian|fasci-di-rette|parabola|ellisse|iperbole|geometria-analitica/', 'out' => '/trasformazioni-e-piano/',
            'blurb' => 'Il piano cartesiano: distanza e punto medio, la retta e i fasci di rette, parabola, circonferenza, ellisse e iperbole con le loro equazioni.'),
        'esponenziali-e-logaritmi' => array('name' => 'Esponenziali e logaritmi',
            'in' => '/esponenzial|logaritm/', 'out' => '/^$/',
            'blurb' => 'Potenze con esponente reale, funzione esponenziale, logaritmi e loro proprietà, equazioni e disequazioni esponenziali e logaritmiche.'),
        'goniometria-e-trigonometria' => array('name' => 'Goniometria e trigonometria',
            'in' => '/goniometr|trigonometr/', 'out' => '/^$/',
            'blurb' => 'Radianti, seno, coseno e tangente, formule goniometriche, equazioni goniometriche, teoremi dei seni e del coseno.'),
        'calcolo-letterale-ed-equazioni' => array('name' => 'Calcolo letterale ed equazioni',
            'in' => '/letterale|monomi|polinomi|equazion|prodotti-notevoli|scomposizion|algebric|sistemi/', 'out' => '/esponenzial|logaritm|goniometr|differenzial/',
            'blurb' => 'Monomi e polinomi, prodotti notevoli, equazioni di primo grado e problemi risolti con le equazioni.'),
        'analisi' => array('name' => 'Limiti, derivate e integrali',
            'in' => '/limiti|continuita|asintot|derivat|calcolo-differenziale|massimi|studio-di-funzione|integral|differenzial|dominio-e-segno/', 'out' => '/^$/',
            'blurb' => 'Analisi per la quinta liceo: dominio e segno, limiti e forme indeterminate, continuità e asintoti, derivate e loro teoremi, massimi e minimi, studio di funzione, integrali ed equazioni differenziali.'),
        'dati-e-probabilita' => array('name' => 'Dati e probabilità',
            'in' => '/dati|probabilit|grafic|indagin|statistic|combinator/', 'out' => '/cartesian/',
            'blurb' => 'Indagini, tabelle, ideogrammi e istogrammi, la moda, eventi certi, possibili e impossibili.'),
    );
}

/* Spain: Spanish unit slugs, Spanish names (LOMLOE) */
function topic_defs_es() {
    return array(
        'numeros' => array('name' => 'Números',
            'in' => '/numeros|numeracion|comparar|contar-hasta|redondeo|romanos|potencias|jerarquia|radicales|logaritmos|notacion-cientifica|propiedades-de-las-operaciones/', 'out' => '/decimal|fraccion|medir/',
            'blurb' => 'Leer, escribir y descomponer números, valor posicional, comparar, ordenar y redondear, números romanos.'),
        'suma-y-resta' => array('name' => 'Suma y resta',
            'in' => '/suma|resta|calculo-mental|agregar-y-quitar/', 'out' => '/fraccion|decimal|riemann/',
            'blurb' => 'Cálculo mental, sumas y restas en vertical con llevadas, estimaciones y problemas de sumar y restar.',
            'blurb_mx' => 'Cálculo mental, sumas y restas en vertical con reagrupación, estimaciones y problemas de sumar y restar.'),
        'multiplicacion-y-division' => array('name' => 'Multiplicación y división',
            'in' => '/multiplica|division|divisiones|tablas-de-multiplicar|multiplos|divisores|repartos|separar-y-repartir|dobles|divisibilidad|mcd-y-mcm/', 'out' => '/fraccion|decimal/',
            'blurb' => 'Tablas de multiplicar, multiplicaciones y divisiones por una y dos cifras, la prueba de la división, múltiplos y divisores.'),
        'fracciones-y-decimales' => array('name' => 'Fracciones y decimales',
            'in' => '/fraccion|decimal|porcentaje|mitad-tercio|mercantil|matematica-financiera/', 'out' => '/proporcionalidad|algebraicas/',
            'blurb' => 'Fracciones de la unidad y de una cantidad, fracciones equivalentes, décimas y centésimas, sumar y restar decimales.'),
        'problemas' => array('name' => 'Problemas',
            'in' => '/problemas/', 'out' => '/^$/',
            'blurb' => 'Problemas de una y dos operaciones con datos de la vida diaria: compras, viajes, recetas y repartos.'),
        'magnitudes-y-medida' => array('name' => 'Magnitudes y medida',
            'in' => '/longitud|masa|capacidad|medida|tiempo|reloj|dinero|monedas|medir|calendario|dias-semanas|perimetro|area|superficie|^volumen$|conversion-de-unidades|volumen-de-/', 'out' => '/poligonos-y-areas|integrales|tendencia-central|con-expresiones|expresiones-algebraicas|dispersion/',
            'blurb' => 'Longitud, masa y capacidad, cambio de unidades, perímetro y área, el reloj y el tiempo, el dinero en euros.',
            'blurb_mx' => 'Longitud, masa y capacidad, cambio de unidades, perímetro y área, el reloj y el tiempo, el dinero en pesos.'),
        'geometria' => array('name' => 'Geometría',
            'in' => '/parabola|elipse|ecuacion-general-de-segundo|leyes-de-senos|euclidiana|fractales|angulos|rectas|poligonos|prismas|piramides|cartesiano|triangulos|cuadrilateros|cuerpos|simetria|coordenadas|figuras|circunferencia|posiciones|orientacion|pitagoras|semejanza|trigonometria|movimientos|analitica|espacio|vectores|conicas|triangulos|planos|distancias|construcciones|esfera|trigonometric/', 'out' => '/^area-|volumenes-de-cuerpos|graficas|perimetro-y-area|volumen-de-/',
            'blurb' => 'Rectas y ángulos, polígonos, triángulos y cuadriláteros, circunferencia y círculo, cuerpos geométricos, simetría y coordenadas.'),
        'algebra-y-proporcionalidad' => array('name' => 'Álgebra y proporcionalidad',
            'in' => '/patrones|ecuaciones|expresiones|proporcionalidad|algebraico|polinomios|inecuaciones|sucesiones|matrices|determinantes|gauss|programacion-lineal|desigualdades|productos-notables|factorizacion|reparto-proporcional|lenguaje-natural|modelacion-algebraica/', 'out' => '/ecuaciones-diferenciales/',
            'blurb' => 'Series y patrones, expresiones con letras, ecuaciones, sistemas e inecuaciones, polinomios, sucesiones y proporcionalidad.'),
        'analisis' => array('name' => 'Límites, derivadas e integrales',
            'in' => '/limites|derivadas|integrales|continuidad|la-derivada|derivacion|optimizacion|origen-del-calculo|razon-de-cambio|recta-tangente|teorema-fundamental|ecuaciones-diferenciales|sumas-de-riemann|integral-indefinida|metodos-numericos|sistemas-dinamicos/', 'out' => '/^$/',
            'blurb' => 'Límites y continuidad, asíntotas, derivadas y sus aplicaciones (máximos, mínimos y optimización), integrales y cálculo de áreas.'),
        'funciones' => array('name' => 'Funciones',
            'in' => '/funciones|coordenadas-y-graficas|variacion-/', 'out' => '/^$/',
            'blurb' => 'Coordenadas y gráficas, dominio, crecimiento, máximos y mínimos, funciones lineales, cuadráticas, exponenciales y logarítmicas.'),
        'estadistica-y-probabilidad' => array('name' => 'Estadística y probabilidad',
            'in' => '/graficos|pictogramas|clasificar-y-registrar|graficas-circulares|tablas-y-graficas|tablas-de|estadistica|probabilidad|media|seguro-posible|combinatoria|distribucion|muestreo|intervalos-de-confianza|tendencia-central|histogramas|interpretacion-de-graficas|eventos|dispersion|correlacion|estudios-observacionales|hipotesis|tecnicas-de-conteo|tipos-de-variables|valores-atipicos|variabilidad-y-toma/', 'out' => '/tablas-de-multiplicar/',
            'blurb' => 'Tablas de frecuencias, gráficos de barras y de líneas, la media y la moda, sucesos seguros, posibles e imposibles.'),
    );
}

/* Brazil: Portuguese unit slugs, Portuguese names (BNCC) */
function topic_defs_br() {
    return array(
        'numeros' => array('name' => 'Números',
            'in' => '/numeros|comparar-e-ordenar|reta-numerica|sequencias|quantidades|dezenas|ordinais|classificar|potencias|radicais|radiciacao|notacao|arredondamento/', 'out' => '/decima|fraco|primos|^sequencias$|sequencias-recursivas/',
            'blurb' => 'Ler, escrever e decompor números até centenas de milhar, valor posicional, comparar, ordenar e arredondar, sequências numéricas.'),
        'fracoes-e-decimais' => array('name' => 'Frações, decimais e porcentagem',
            'in' => '/fraco|decima|decimos|dizimas|porcentage|metade-terca|juros/', 'out' => '/^$/',
            'blurb' => 'Metade, terça e quarta parte, frações e números mistos, frações equivalentes, números decimais até os milésimos, comparar frações e decimais, porcentagem.'),
        'adicao-e-subtracao' => array('name' => 'Adição e subtração',
            'in' => '/adicao|subtracao|calculo-mental|igualdade|relacoes-entre/', 'out' => '/partilha/',
            'blurb' => 'Cálculo mental, adição e subtração com reagrupamento e com decimais, conta armada, prova real, igualdade e termo desconhecido, problemas.'),
        'multiplicacao-e-divisao' => array('name' => 'Multiplicação e divisão',
            'in' => '/multiplica|divisao|tabuada|metade|terca|dobro|proporcionalidade|relacoes-entre|propriedades|multiplos|mmc|operacoes-com-numeros/', 'out' => '/principio/',
            'blurb' => 'Tabuada, multiplicação e divisão com números naturais e decimais, método da chave e resto, proporcionalidade e partilha em partes desiguais.'),
        'geometria' => array('name' => 'Geometria',
            'in' => '/figuras|solidos|localizacao|trajetos|simetria|angulos|poligonos|cartesiano|ampliacao|prismas|piramides|semelhanca|pitagoras|relacoes-metricas|distancia|vistas|retas|circunferencia|transformacoes-geometricas|mediatriz|isometricas|cilindros|trigonometria-no|leis-dos-senos/', 'out' => '/^$/',
            'blurb' => 'Localização, trajetos e plano cartesiano, figuras espaciais e planificações, prismas e pirâmides, polígonos e ângulos, ampliação e redução.'),
        'grandezas-e-medidas' => array('name' => 'Grandezas e medidas',
            'in' => '/comprimento|massa|capacidade|area|perimetro|volume|horas|tempo|temperatura|sistema-monetario|dinheiro|medida|calendario|periodos|grandezas-compostas|cilindros|superficies|escalas/', 'out' => '/tendencia/',
            'blurb' => 'Comprimento, massa e capacidade, transformação de unidades, perímetro, área e volume, horas e intervalos de tempo, o sistema monetário brasileiro.'),
        'algebra-e-funcoes' => array('name' => 'Álgebra e funções',
            'in' => '/funcoes|equacoes|produtos-notaveis|fatoracao|grandezas-proporcionais|razoes-entre|partilha|algebrica|proporcionalidade-direta|^sequencias$|sequencias-recursivas|funcao|progressao|sistemas-lineares|logaritmos|maximo-e-minimo/', 'out' => '/^$/',
            'blurb' => 'Funções e gráficos, razões entre grandezas, grandezas diretamente e inversamente proporcionais, produtos notáveis, fatoração e equações do 2º grau.'),
        'probabilidade-e-estatistica' => array('name' => 'Probabilidade e estatística',
            'in' => '/graficos|tabelas|probabilidade|pesquisa|contagem|principio-multiplicativo|principio-fundamental|permutacoes|(^|-)media(-|$)|tendencia|correlacao|histograma|box-plot/', 'out' => '/^$/',
            'blurb' => 'Tabelas de dupla entrada, gráficos de colunas e de linhas, pesquisas, problemas de contagem, espaço amostral e probabilidade como fração.'),
        'trigonometria' => array('name' => 'Trigonometria',
            'in' => '/trigonometri|senos|seno-e-cosseno/', 'out' => '/^$/',
            'blurb' => 'Seno, cosseno e tangente no triângulo retângulo, ângulos notáveis, leis dos senos e dos cossenos, ciclo trigonométrico, radianos e funções periódicas.'),
        'matematica-financeira' => array('name' => 'Matemática financeira',
            'in' => '/juros|orcamento|financiamento|taxas-e-indices/', 'out' => '/^$/',
            'blurb' => 'Acréscimos e descontos, juros simples e compostos, compras à vista e a prazo, orçamento doméstico, inflação e índices socioeconômicos.'),
    );
}

/* Türkiye (tr): Türkiye Yüzyılı Maarif Modeli. Slugs are Turkish */
function topic_defs_tr() {
    return array(
        'sayilar' => array('name' => 'Sayılar ve Basamak Değeri',
            'in' => '/sayilar|siralama|yuvarlama|ritmik|tek-ve-cift|basamak|buyuk-sayilar|nesne-sayisini|sayi-araliklari|sayi-kumeleri|nesne-sayma|bir-bakista/', 'out' => '/islem|asal|ondalik|kesir|toplama|cikarma|rasyonel|tam-sayilar|ispat|logaritm/',
            'blurb' => 'Sayıları okuma ve yazma, basamak ve bölük, basamak değeri, sayıları karşılaştırma, sıralama ve yuvarlama, ritmik sayma, büyük sayılar ve doğal sayılarla problemler.'),
        'toplama-ve-cikarma' => array('name' => 'Toplama ve Çıkarma',
            'in' => '/toplama|cikarma|artma-ve-azalma|butun-ve-parca/', 'out' => '/veri|kesir|rasyonel/',
            'blurb' => 'Eldeli toplama, onluk bozarak çıkarma, zihinden işlem, tahmin ve sonucu kontrol etme.'),
        'carpma-ve-bolme' => array('name' => 'Çarpma ve Bölme',
            'in' => '/carpma|bolme|dort-islem|islem-onceligi|paylastirma/', 'out' => '/kesir|ondalik|bolunebilme|bolenler|rasyonel|fonksiyon|polinom/',
            'blurb' => 'Çarpım tablosu, çok basamaklı çarpma ve bölme, kalanlı bölme, zihinden işlem ve kısa yollar, işlem önceliği ve dört işlem problemleri.'),
        'carpanlar-ve-bolunebilme' => array('name' => 'Çarpanlar, Katlar ve Bölünebilme',
            'in' => '/asal|bolunebilme|carpanlar-ve-katlar|ortak-bolenler|ebob/', 'out' => '/^$/',
            'blurb' => 'Çarpanlar ve katlar, 2, 3, 4, 5, 6, 9 ve 10 ile bölünebilme, asal sayılar ve asal çarpanlar, ortak bölenler ve ortak katlar.'),
        'rasyonel-sayilar' => array('name' => 'Tam Sayılar ve Rasyonel Sayılar',
            'in' => '/rasyonel|tam-sayilar/', 'out' => '/fonksiyon|polinom/',
            'blurb' => 'Tam sayılar ve mutlak değer, rasyonel sayılar ve sayı doğrusu, sonlu ve devirli ondalık gösterim, karşılaştırma ve sıralama, rasyonel sayılarla dört işlem ve problemler.'),
        'kesirler' => array('name' => 'Kesirler, Ondalık Gösterim ve Yüzde',
            'in' => '/kesir|kesri|ondalik|yuzde|gosterimleri|yarim-ve-ceyrek/', 'out' => '/rasyonel/',
            'blurb' => 'Birim, basit, bileşik ve tam sayılı kesirler, denk kesirler, kesirlerle işlemler, ondalık gösterim, yüzdeler ve farklı gösterimleri karşılaştırma.'),
        'oruntuler-ve-esitlik' => array('name' => 'Örüntüler, Eşitlik ve Cebir',
            'in' => '/oruntu|esitlik|cebir|algoritma|algoritmik|islem-ozellikleri/', 'out' => '/dogrusal/',
            'blurb' => 'Sayı ve şekil örüntülerinin kuralı, eşitlik ve işlem özellikleri, algoritmalar, cebirsel ifadeler ve örüntülerin cebirle gösterimi.'),
        'oran-ve-oranti' => array('name' => 'Oran ve Orantı',
            'in' => '/(^|-)oran(-|$)|oranti/', 'out' => '/^$/',
            'blurb' => 'Birimli ve birimsiz oran, denk oranlar ve birim oran, orantılı çokluklar ve orantı sabiti, doğru orantı problemleri ve verilen oranda paylaştırma.'),
        'denklemler-ve-esitsizlikler' => array('name' => 'Denklemler ve Eşitsizlikler',
            'in' => '/denklem|esitsizlik/', 'out' => '/ucgen-esitsizligi|ustel|logaritm|trigonometri|polinom/',
            'blurb' => 'Birinci dereceden bir bilinmeyenli denklemler ve eşitsizlikler, çözüm kümesini sayı doğrusunda gösterme, yaş, ardışık sayı ve fiyat problemleri.'),
        'uslu-ve-karekoklu-ifadeler' => array('name' => 'Üslü ve Kareköklü İfadeler',
            'in' => '/uslu|bilimsel-gosterim|karekok|koklu/', 'out' => '/fonksiyon/',
            'blurb' => 'Üslü ifadeler ve üslü ifadelerle işlemler, 10’un kuvvetleri ve bilimsel gösterim, tam kare sayılar, kareköklü ifadeler ve sadeleştirme.'),
        'dogrusal-fonksiyonlar' => array('name' => 'Doğrusal Fonksiyonlar',
            'in' => '/dik-koordinat|dogrusal|egim|mutlak-deger-fonksiyonu/', 'out' => '/denklem/',
            'blurb' => 'Dik koordinat sistemi, doğrusal ilişkiler ve fonksiyonlar, tablo, denklem ve grafik, eğim, iki doğrunun kesişmesi ve doğrusal fonksiyon problemleri.'),
        'olcme' => array('name' => 'Ölçme',
            'in' => '/olcme|olcu|saat|paralar|uzunlug|cevre|kutle|alan|cember-uzunlugu|hacim|hacmi/', 'out' => '/(^|-)aci|veri|kalan/',
            'blurb' => 'Uzunluk, kütle, sıvı ve zaman ölçme, birim dönüşümleri, paralarımız, çevre uzunluğu, alan ve alan ölçü birimleri, çember uzunluğu.'),
        'geometri' => array('name' => 'Geometri',
            'in' => '/geometrik|simetri|sekil|cisim|aci|ucgen|dortgen|cokgen|paralel|dogrularin|kup|yansima|eslik|benzerlik|pisagor|oteleme|konum|cemberin|cemberde|cember-ve-daire|prizma-ve-silindir|piramit-koni/', 'out' => '/alani|olasilik|cevre|hacim|hacmi|trigonometri|diziler|turev/',
            'blurb' => 'Geometrik cisimler ve açınımları, üçgen ve dörtgenler, çokgenler, açılar ve açı ölçme, paralel doğrular, çember, simetri.'),
        'veri' => array('name' => 'Veri',
            'in' => '/veri|grafik|tablo/', 'out' => '/dogrusal|trigonometri/',
            'blurb' => 'Veri toplama, çetele ve sıklık tablosu, sütun, nokta ve daire grafiği, aritmetik ortalama, medyan, tepe değer ve dal-yaprak gösterimi.'),
        'olasilik' => array('name' => 'Olasılık',
            'in' => '/olasilik|imkansiz|olaylar|sayma-stratejileri|bayes/', 'out' => '/^$/',
            'blurb' => 'İmkânsız, olabilir ve kesin olaylar, deneysel ve teorik olasılık, sayma stratejileri, permütasyon ve kombinasyon, koşullu olasılık ve Bayes teoremi.'),
        'fonksiyonlar' => array('name' => 'Fonksiyonlar',
            'in' => '/fonksiyon/', 'out' => '/dogrusal|mutlak-deger|trigonometri|ustel|logaritm|diziler/',
            'blurb' => 'Fonksiyon olma şartları, tanım ve görüntü kümesi, karesel, karekök ve rasyonel fonksiyonlar, ters fonksiyon ve fonksiyonlarla modelleme.'),
        'diziler-ve-polinomlar' => array('name' => 'Diziler ve Polinomlar',
            'in' => '/diziler|polinom/', 'out' => '/^$/',
            'blurb' => 'Aritmetik ve geometrik diziler, genel terim ve indirgeme, dizilerin toplamı, polinomlar, polinom bölmesi ve kalan teoremi, polinom ve rasyonel denklemler.'),
        'limit-ve-turev' => array('name' => 'Limit ve Türev',
            'in' => '/limit|sureklilik|turev/', 'out' => '/^$/',
            'blurb' => 'Limit, soldan ve sağdan limit, 0/0 belirsizliği, süreklilik, türevin tanımı, türev kuralları, teğet doğrusu, artanlık, ekstremum ve optimizasyon.'),
        'ustel-ve-logaritmik-fonksiyonlar' => array('name' => 'Üstel ve Logaritmik Fonksiyonlar',
            'in' => '/ustel|logaritm/', 'out' => '/^$/',
            'blurb' => 'Üstel fonksiyonlar, büyüme ve azalma, logaritma ve özellikleri, logaritmik fonksiyonlar, üstel ve logaritmik denklemler ve eşitsizlikler.'),
        'trigonometri' => array('name' => 'Trigonometri',
            'in' => '/trigonometri|sinus-ve-kosinus/', 'out' => '/^$/',
            'blurb' => 'Dik üçgende sinüs, kosinüs, tanjant ve kotanjant, özel açılar, özdeşlikler, sinüs ve kosinüs teoremleri, birim çember, trigonometrik fonksiyonlar, grafikler ve denklemler.'),
    );
}

/* Indonesia (id): Kurikulum Merdeka, CP 2025. Slugs are Indonesian */
function topic_defs_id() {
    return array(
        'bilangan-cacah' => array('name' => 'Bilangan Cacah dan Nilai Tempat',
            'in' => '/^bilangan|membilang|urutan-bilangan|membandingkan-banyak|membandingkan-dan-mengurutkan-bilangan|menyusun-dan-menguraikan-bilangan|nilai-tempat|pembulatan|puluhan-dan-satuan/', 'out' => '/^bilangan-(bulat|rasional|berpangkat|kompleks)/',
            'blurb' => 'Membaca dan menulis bilangan, nilai tempat ribuan, ratusan, puluhan, dan satuan, membandingkan dan mengurutkan bilangan, serta menyusun dan menguraikan bilangan.'),
        'penjumlahan-dan-pengurangan' => array('name' => 'Penjumlahan dan Pengurangan',
            'in' => '/penjumlahan|pengurangan|menambah|mengurangi/', 'out' => '/pecahan|desimal/',
            'blurb' => 'Penjumlahan dan pengurangan bersusun dengan menyimpan dan meminjam, berhitung cepat, dan memeriksa jawaban.'),
        'perkalian-dan-pembagian' => array('name' => 'Perkalian dan Pembagian',
            'in' => '/perkalian|pembagian|membagi|faktor|kelipatan|kpk|fpb|operasi-hitung-campuran/', 'out' => '/pecahan|desimal|faktorisasi/',
            'blurb' => 'Perkalian dan pembagian sampai 100, hubungan perkalian dan pembagian, serta faktor dan kelipatan suatu bilangan.'),
        'pecahan-desimal-dan-persen' => array('name' => 'Pecahan, Desimal, dan Persen',
            'in' => '/pecahan|desimal|persen|setengah|aritmetika-sosial|bunga-majemuk/', 'out' => '/^$/',
            'blurb' => 'Pecahan berpembilang satu, pecahan berpenyebut sama, pecahan senilai, desimal persepuluhan dan perseratusan, serta hubungannya dengan persen.'),
        'soal-cerita' => array('name' => 'Soal Cerita',
            'in' => '/soal-cerita|(^|-)uang(-|$)/', 'out' => '/^$/',
            'blurb' => 'Masalah sehari-hari dengan uang, belanja, dan benda di sekitar kita yang diselesaikan dengan empat operasi hitung.'),
        'aljabar-dan-pola' => array('name' => 'Aljabar dan Pola',
            'in' => '/pola|kalimat-matematika|perbandingan|rasio|persamaan|kesamaan|lompat-hitung|bentuk-aljabar|barisan|polinomial|matriks/', 'out' => '/linear|kuadrat|garis-lurus|rasional|trigonometri|lingkaran/',
            'blurb' => 'Mencari nilai yang belum diketahui dalam kalimat matematika, serta mengenali dan melanjutkan pola gambar dan pola bilangan.'),
        'pengukuran' => array('name' => 'Pengukuran',
            'in' => '/pengukuran|membandingkan-ukuran|panjang|berat|luas|volume|waktu|keliling|mengukur|prisma|tabung/', 'out' => '/^bangun-datar$|^menyusun|^bangun-ruang|sudut|segi-empat|aturan-sinus|integral/',
            'blurb' => 'Mengukur panjang dan berat dengan satuan baku, hubungan cm dan m serta g dan kg, luas dengan persegi satuan, dan volume dengan kubus satuan.'),
        'geometri' => array('name' => 'Geometri',
            'in' => '/bangun|mengenal-bentuk|sudut|garis|simetri|kubus|balok|peta|arah-mata-angin|posisi|segitiga|sebangun|kongruen|lingkaran|transformasi|dilatasi|pythagoras|vektor|dimensi-tiga/', 'out' => '/(?<!sudut-)keliling|^luas-|garis-lurus|komposisi-fungsi|aturan-sinus/',
            'blurb' => 'Ciri-ciri segitiga, segiempat, dan segi banyak, sisi dan sudut, serta menyusun dan menguraikan bangun datar.'),
        'data-dan-peluang' => array('name' => 'Data dan Peluang',
            'in' => '/piktogram|diagram|(^|-)data(-|$)|peluang|kemungkinan|statistika|korelasi|simpangan|pencacahan|permutasi/', 'out' => '/datar/',
            'blurb' => 'Membaca, menyajikan, dan membandingkan data dalam tabel, piktogram, dan diagram batang.'),
        'bilangan-bulat-dan-rasional' => array('name' => 'Bilangan Bulat dan Rasional',
            'in' => '/^(operasi-)?bilangan-(bulat|rasional)$/', 'out' => '/^$/',
            'blurb' => 'Bilangan negatif pada garis bilangan, membandingkan dan mengurutkan, serta operasi hitung bilangan bulat, pecahan, dan desimal bertanda.'),
        'pangkat-dan-akar' => array('name' => 'Bilangan Berpangkat dan Bentuk Akar',
            'in' => '/berpangkat|notasi-ilmiah|bentuk-akar|^eksponen$|^logaritma$/', 'out' => '/^$/',
            'blurb' => 'Sifat-sifat perpangkatan, pangkat nol, negatif, dan pecahan, notasi ilmiah, bentuk akar, serta logaritma dan sifat-sifatnya.'),
        'persamaan-dan-fungsi' => array('name' => 'Persamaan, Pertidaksamaan, dan Fungsi',
            'in' => '/linear|persamaan-kuadrat|fungsi|garis-lurus/', 'out' => '/regresi|trigonometri|^limit|^turunan/',
            'blurb' => 'Persamaan dan pertidaksamaan linear, SPLDV, relasi dan fungsi, gradien dan persamaan garis lurus, serta persamaan dan fungsi kuadrat.'),
        'diziler-ve-polinomlar' => array('name' => 'Diziler ve Polinomlar',
            'in' => '/diziler|polinom/', 'out' => '/^$/',
            'blurb' => 'Aritmetik ve geometrik diziler, genel terim ve indirgeme, dizilerin toplamı, polinomlar, polinom bölmesi ve kalan teoremi, polinom ve rasyonel denklemler.'),
        'limit-ve-turev' => array('name' => 'Limit ve Türev',
            'in' => '/limit|sureklilik|turev/', 'out' => '/^$/',
            'blurb' => 'Limit, soldan ve sağdan limit, 0/0 belirsizliği, süreklilik, türevin tanımı, türev kuralları, teğet doğrusu, artanlık, ekstremum ve optimizasyon.'),
        'ustel-ve-logaritmik-fonksiyonlar' => array('name' => 'Üstel ve Logaritmik Fonksiyonlar',
            'in' => '/ustel|logaritm/', 'out' => '/^$/',
            'blurb' => 'Üstel fonksiyonlar, büyüme ve azalma, logaritma ve özellikleri, logaritmik fonksiyonlar, üstel ve logaritmik denklemler ve eşitsizlikler.'),
        'trigonometri' => array('name' => 'Trigonometri',
            'in' => '/trigonometri|aturan-sinus/', 'out' => '/^$/',
            'blurb' => 'Perbandingan sinus, kosinus, dan tangen, sudut istimewa dan sudut berelasi, aturan sinus dan kosinus, serta grafik dan persamaan fungsi trigonometri.'),
        'kalkulus' => array('name' => 'Limit, Turunan, dan Integral',
            'in' => '/^limit|turunan|integral/', 'out' => '/^$/',
            'blurb' => 'Limit fungsi aljabar, turunan dan penggunaannya untuk garis singgung, titik stasioner, dan optimasi, serta integral tak tentu, integral tentu, dan luas daerah.'),
    );
}

function topic_defs_se() {
    return array(
        'tal' => array('name' => 'Tal och positionssystemet',
            'in' => '/tal-till|rakna-till|jamfora|ordna|overslag|avrund|positions|negativa-tal|stora-tal|talkamrat|talraden|tiotal-och|udda/', 'out' => '/talfoljd|brak|decimal/',
            'blurb' => 'Hundratal, tiotal och ental, att läsa, skriva, jämföra och ordna tal, tallinjen, avrundning, överslagsräkning och rimlighet.'),
        'addition-och-subtraktion' => array('name' => 'Addition och subtraktion',
            'in' => '/addition|subtraktion|huvudrakning|lagga-till|ta-bort/', 'out' => '/brak|decimal/',
            'blurb' => 'Tiokamrater och hundrakamrater, huvudräkning, uppställning med minnessiffra och växling, kontroll med det motsatta räknesättet och textuppgifter.'),
        'multiplikation-och-division' => array('name' => 'Multiplikation och division',
            'in' => '/multiplikation|division|dubbelt|prioritering|delning/', 'out' => '/brak|decimal|normalfordelning/',
            'blurb' => 'Lika stora grupper, multiplikationstabellerna, division som delning och innehåll, division med rest, dubbelt och hälften och textuppgifter.'),
        'brak-decimaltal-och-procent' => array('name' => 'Bråk, decimaltal och procent',
            'in' => '/brak|decimal|procent|ranta|exponentiell|halvor|fjardedel|forandringsfaktor/', 'out' => '/^$/',
            'blurb' => 'Bråk och decimaltal, procent och förändringsfaktor, moms, ränta och lån och exponentiell förändring.'),
        'algebra' => array('name' => 'Algebra och mönster',
            'in' => '/(^|-)likhet|monster|talfoljd|ekvation|uttryck|programmering|instruktioner|parenteser|formler|olikheter|kvadrering|faktorisering|(^|-)polynom|komplexa/', 'out' => '/rata-linjen|differential|trigonometri|rekursiva/',
            'blurb' => 'Likhetstecknets betydelse, saknade tal, mönster och talföljder, uttryck med variabler, parenteser, formler, ekvationer, olikheter och ekvationssystem.'),
        'matning' => array('name' => 'Mätning, tid och pengar',
            'in' => '/langd|massa|volym|klockan|(^|-)tid(-|$)|pengar|omkrets|area|enheter|prisma|pyramid/', 'out' => '/kroppar|integral/',
            'blurb' => 'Längd, massa och volym med vanliga enheter, klockan och pengar, omkrets och area, volym och begränsningsarea av prisma, cylinder, pyramid, kon och klot.'),
        'geometri' => array('name' => 'Geometri',
            'in' => '/geometrisk|symmetri|lagesord|vinkl|kroppar|figurer|cirkel|pythagoras|likformighet|(^|-)former(-|$)/', 'out' => '/enhetscirkeln/',
            'blurb' => 'Trianglar, fyrhörningar och cirklar, vinklar och polygoner, kroppar, symmetri, likformighet, Pythagoras sats och cirkelsektorer.'),
        'statistik-och-sannolikhet' => array('name' => 'Statistik och sannolikhet',
            'in' => '/tabell|diagram|slump|sannolikhet|statistik|lagesmatt|spridningsmatt|medelvarde|kombinatorik|sortera|standardavvikelse|normalfordelning|regression/', 'out' => '/tabellerna/',
            'blurb' => 'Streckräkning, tabeller och stapel-, linje- och cirkeldiagram, medelvärde, typvärde och median, slump och sannolikhet och kombinatorik.'),
        'samband-och-forandring' => array('name' => 'Proportionalitet, funktioner och grafer',
            'in' => '/proportionalitet|skala|koordinat|funktion|grafer|rata-linjen/', 'out' => '/primitiva|asymptot|natverk|trigonometri/',
            'blurb' => 'Proportionella samband, jämförpris och fart, skala, koordinatsystem, funktioner, linjära funktioner och räta linjens ekvation och att tolka grafer.'),
        'potenser-och-reella-tal' => array('name' => 'Potenser, primtal och reella tal',
            'in' => '/potens|reella|kvadratrot|delbarhet|primtal|logaritm|(^|-)rotter/', 'out' => '/potensekvation/',
            'blurb' => 'Delbarhet och primtal, potenser och kvadratrötter, potenslagar, grundpotensform och prefix samt rationella och irrationella tal.'),
        'trigonometri' => array('name' => 'Trigonometri och vektorer',
            'in' => '/trigonometri|triangelsatser|enhetscirkeln|vektorer/', 'out' => '/^$/',
            'blurb' => 'Sinus, cosinus och tangens, sinus-, cosinus- och areasatsen, enhetscirkeln och radianer, trigonometriska formler, ekvationer och grafer samt vektorer.'),
        'derivata-och-integraler' => array('name' => 'Derivata och integraler',
            'in' => '/gransvarden|derivat|deriver|tangenter|extrempunkt|optimering|primitiva|integral|kedjeregeln|kvotregeln|talet-e|differentialekv|asymptoter/', 'out' => '/^$/',
            'blurb' => 'Gränsvärden, derivatans definition och deriveringsregler, tangenter, extrempunkter och optimering, primitiva funktioner, integraler, rotationsvolymer och differentialekvationer.'),
        'diskret-matematik' => array('name' => 'Diskret matematik, logik och bevis',
            'in' => '/mangdlara|talteori|talbaser|bevis|logik|natverk|rekursiva/', 'out' => '/^$/',
            'blurb' => 'Logik och bevismetoder, induktion, mängdlära, talteori och kongruensräkning, talbaser, rekursiva talföljder och grafteori.'),
        'problemlosning' => array('name' => 'Problemlösning',
            'in' => '/problemlosning/', 'out' => '/^$/',
            'blurb' => 'Textuppgifter och problem i flera steg, att räkna baklänges, pröva systematiskt, hitta mönster och bedöma om svaret är rimligt.'),
    );
}

/* Science (US NGSS first). Slugs are English; the same topics can serve other English-speaking countries later */
function topic_defs_science($country = null) {
    return array(
        'matter' => array('name' => 'Matter and Its Properties', 'in' => '/^ionic-and-covalent-compounds$|^elements-and-compounds$|^gases-and-atmospheric-chemistry$|^solids-and-liquids$|^fluids-density-and-buoyancy$|^fluid-pressure-and-technology$|^chemical-synthesis-and-analysis$|^oxidation-and-reduction$|^electrochemical-cells$|^the-standard-model$|^ionising-radiation-and-nuclear-reactions$|matter|reversible|changes-of-state|solids-liquids|particle|material|mixture|solution|chemical-change|physical-change|conservation-of-mass|states-of|atom|molecule|reaction|small-pieces|heating-and-cooling|equation|bonding|equilibrium|nuclear|periodic|stoichiometry|the-mole|isotope|intermolecular|materials|acids-and|metals-and|extraction|quantitative|chemical-analysis|organic|kinetics|acids-bases|transition-metals|carbon-and-its|separation|acidic-basic|physical-and-chemical|world-of-things|making-things|things-are-made|basic-concepts-of-chemistry|classification-of-elements|^redox-reactions$|^hydrocarbons$|chemical-thermodynamics|^kinetic-theory$|properties-of-solids|properties-of-fluids|haloalkanes|^alcohols-phenols|aldehydes-ketones|^amines$|coordination-compounds|d-and-f-block|electrochemistry|^nuclei$|semiconductor|^radioactivity$|experimental-chemistry|chemical-calculations|acid-base-chemistry|qualitative-analysis|redox-chemistry|chemical-energetics/', 'out' => '/^static-equilibrium-and-torque$|^climate-change-impacts-and-solutions$|cycl|food|light-and|radiation|duality|nuclear-fusion|earth-materials|biological-molecules|mechanics-and-materials|anatomy|system-of-particles|^biomolecules$/',
            'blurb' => 'What matter is made of, how to identify materials by their properties, mixtures and solutions, physical and chemical changes, and why mass is conserved.'),
        'forces-and-motion' => array('name' => 'Forces and Motion', 'in' => '/^simple-machines-and-power$|^static-equilibrium-and-torque$|^simple-machines$|^forces-of-flight$|^flight-in-nature-and-technology$|^systems-and-mechanical-advantage$|^fluid-pressure-and-technology$|^special-relativity$|force|motion|gravity|magnet|push|pull|newton|speed-and-direction|momentum|impulse|resistance|friction|lever|^pressure$|moments|mechanics|gravitational|^gravitation$|^how-things-work$|rotational-motion|objects-move|properties-of-solids|properties-of-fluids|^oscillations$|electric-charges|^kinematics$|^dynamics$|turning-effect/', 'out' => '/intermolecular|radiation|electromagnetic-spectrum|locomotion|electromagnetic-waves/',
            'blurb' => 'Pushes and pulls, balanced and unbalanced forces, gravity, magnets and how forces change the way objects move.'),
        'energy' => array('name' => 'Energy', 'in' => '/^systems-and-mechanical-advantage$|^ionising-radiation-and-nuclear-reactions$|energy|light|sound|heat|electric|wave|circuit|collision|information|signal|shade|voltage|conductors-and-insulators|pitch|thermal|capacitor|^temperature-and|^thermodynamics$|chemical-thermodynamics|^kinetic-theory$|alternating-current|electrostatic-potential|^nuclei$|semiconductor|^radioactivity$|electromagnetic-induction|chemical-energetics/', 'out' => '/^earthquakes-and-seismic-waves$|^light-and-reflection$|^the-wave-nature-of-light$|flight|light-reflection|waves-sound-and-light|heating-and-cooling|daylight|momentum|impulse|coulomb|genetic-information/',
            'blurb' => 'Forms of energy and how it moves: light, sound, heat and electricity, energy in food, and energy from the sun.'),
        'waves-and-light' => array('name' => 'Waves, Light and Information', 'in' => '/^refraction-and-lenses$|^revolutions-in-modern-physics$|^quantum-theory$|wave|light|information|signal|sound-and-vibration|radiation|how-we-see|reflection|pitch|sounds-are-made|^shadows$|^sound$|human-eye|^oscillations$|ray-optics|electromagnetic-spectrum/', 'out' => '/^earthquakes-and-seismic-waves$|flight|^ionising-radiation-and-nuclear-reactions$|sunlight|daylight|genetic-information/',
            'blurb' => 'Amplitude and wavelength, how light reflects into our eyes so we can see, and how patterns and codes send information.'),
        'living-things-and-ecosystems' => array('name' => 'Living Things and Ecosystems', 'in' => '/^health-disease-and-immunity$|^biomes$|^sensing-and-responding$|^tissues-organs-and-systems$|^biochemistry$|^metabolic-processes$|^infectious-disease-and-immunity$|plant|animal|food-web|food-chain|ecosystem|decomposer|life-cycle|habitat|trait|inherit|cell|organism|body|senses|structure|past-environment|variation|survival|environmental-change|animal-group|photosynth|respiration|population|biodiversity|energy-flow|reproduction|gene|mutation|selection|embryo|fossil-record|pollinat|offspring|living-things|dna|evolution|behavior|homeostasis|levels-of-organization|punnett|heredity|carbon-cycle|macromolecule|classif|circulatory|diet-|nutrient|^fossils$|micro-organism|growing-up|changing-environments|teeth|digestive|nutrition|skeleton|fossils-are|living-dead|seeds-and-bulbs|staying-healthy|carnivore|evergreen|digestion|gas-exchange|health-and-drugs|infection|enzyme|^ecology$|biological-molecules|exchange-and-transport|life-processes|control-and-coordination|our-environment|unit-of-life|^tissues$|food-resources|living-world|living-creatures|adolescence|^health-the|nature-works|food-we-eat|living-in-harmony|nature-trail|food-for-health|healthy-living|mystery-of-food|our-shared-home|breathing-and-exchange|chemical-coordination|excretory-products|locomotion|^biomolecules$|biotechnology|human-health|microbes-in-human|reproductive-health|adaptation|mans-impact|reproductive-system|movement-of-substances|transport-in-humans|excretion-in-humans|infectious-diseases|nervous-and-endocrine/', 'out' => '/^structure-and-properties-of-matter$|^revolutions-in-modern-physics$|^everyday-structures$|^strong-and-stable-structures$|^forces-acting-on-structures$|^electrochemical-cells$|shade|bonding-and-structure|atomic-structure|structure-of-the-atom|molecular-structure|climate-and-energy|structure-of-atom|classification-of-elements|general-wave/',
            'blurb' => 'How plants and animals get what they need to grow, food chains and food webs, decomposers, and how matter and energy move through an ecosystem.'),
        'earth-and-space' => array('name' => 'Earth and Space', 'in' => '/^space-exploration-and-extreme-environments$|^space-exploration$|sun|star|moon|shadow|day-and-night|sky|planet|solar-system|constellation|season|big-bang|kepler|orbit|universe|day-length|^space$|gravity-and-space|beyond-earth|time-with-the-skies|rhythms-of-nature/', 'out' => '/food|energy|sunlight|reflection|our-home-earth|light-and-shadows/',
            'blurb' => 'The sun, moon and stars, shadows, day and night, seasonal patterns in the sky, and how distance changes how bright a star looks.'),
        'earths-systems' => array('name' => 'Earth’s Systems and Resources', 'in' => '/^surface-processes$|^gases-and-atmospheric-chemistry$|^soils-and-the-environment$|^biogeochemical-cycles$|^managing-environmental-impacts$|earth|water|weather|climate|rock|erosion|landform|hazard|resource|ocean|plate|tecton|human-impact|geologic|fossils-are|^soils$|four-seasons|atmosphere|natures-treasures|cyclone|charge-of-waste|different-lands|journey-of-a-river|mans-impact|air-quality|^the-carbon-cycle$|seasonal-changes/', 'out' => '/earth-and-the-sky|earth-and-space|earth-sun|beyond-earth|food-resources|population|earth-moon|sunlight-warms|nutrients-and-water|resistance|water-moves|our-shared-home/',
            'blurb' => 'The geosphere, hydrosphere, atmosphere and biosphere, where Earth’s water is, weather and climate, and how people protect Earth’s resources.'),
        'engineering-design' => array('name' => 'Engineering Design', 'in' => '/^everyday-structures$|^strong-and-stable-structures$|^form-and-function$|^forces-acting-on-structures$|engineer|design/', 'out' => '/genetic-engineering/',
            'blurb' => 'Define a problem with criteria and constraints, compare possible solutions, and plan fair tests to improve a design.'),
        'working-scientifically' => array('name' => 'Working Scientifically', 'in' => '/working-scientifically|world-of-science|scientific-endeavour|physical-quantities/', 'out' => '/^$/',
            'blurb' => 'Fair tests and variables, careful measurement, repeat readings, tables and graphs, predictions and conclusions based on evidence.'),
    );
}

function topic_defs($country = null, $subject = null) {
    if ($subject === 'science') return topic_defs_science($country);
    if ($country === 'br') return topic_defs_br();
    if ($country === 'es' || $country === 'mx') return topic_defs_es();
    if ($country === 'tw') return topic_defs_tw();
    if ($country === 'cn') return topic_defs_cn();
    if ($country === 'kr') return topic_defs_kr_all();
    if ($country === 'de') return topic_defs_de();
    if ($country === 'ch') return topic_defs_ch();
    if ($country === 'fr') return topic_defs_fr();
    if ($country === 'it') return topic_defs_it();
    if ($country === 'id') return topic_defs_id();
    if ($country === 'tr') return topic_defs_tr();
    if ($country === 'se') return topic_defs_se();
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
            'in' => '/circle|circum|arc-length|arcs-and|sector|chords-and-tangents/', 'out' => '/circle-graph|bisector/',
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
            'in' => '/probab|chance|sample-spaces|likelihood|permutations-and-combinations|expected-value|^venn-diagrams/', 'out' => '/^$/',
            'blurb' => 'Likelihood words, spinners and number cubes, probability as a fraction, experiments and tree diagrams.'),
    );
    if ($country === 'ng') {
        // Nigeria (NERDC topic names): open sentences are algebra, LCM is factors and multiples, decimal fractions are decimals
        $d['algebra']['in'] = substr($d['algebra']['in'], 0, -1) . '|open-sentences/';
        $d['factors-and-multiples']['in'] = substr($d['factors-and-multiples']['in'], 0, -1) . '|lowest-common-multiple/';
        $d['multiplication']['out'] = substr($d['multiplication']['out'], 0, -1) . '|lowest-common-multiple/';
        $d['fractions']['out'] = substr($d['fractions']['out'], 0, -1) . '|^decimal-fractions$/';
        // Primary 1 to JSS 3: directed numbers, commercial arithmetic, variation, number bases
        $d['integers']['in'] = substr($d['integers']['in'], 0, -1) . '|directed-numbers/';
        $d['factors-and-multiples']['in'] = substr($d['factors-and-multiples']['in'], 0, -1) . '|lcm-and-hcf/';
        $d['place-value']['in'] = substr($d['place-value']['in'], 0, -1) . '|tens-and-units/';
        $d['money']['in'] = substr($d['money']['in'], 0, -1) . '|commercial-arithmetic|compound-interest/';
        $d['rounding-and-estimation']['in'] = substr($d['rounding-and-estimation']['in'], 0, -1) . '|approximation/';
        $d['ratios-and-rates']['in'] = substr($d['ratios-and-rates']['in'], 0, -1) . '|^variation$/';
        $d['algebra']['in'] = substr($d['algebra']['in'], 0, -1) . '|quantitative-reasoning/';
        $d['shapes']['out'] = substr($d['shapes']['out'], 0, -1) . '|counting-objects/';
        $d['measurement']['out'] = substr($d['measurement']['out'], 0, -1) . '|central-tendency|area-and-volume-of-solids/';
        $d['area-and-perimeter']['out'] = substr($d['area-and-perimeter']['out'], 0, -1) . '|area-and-volume-of-solids/';
        // SSS 1 to 3
        $d['data-and-graphs']['in'] = substr($d['data-and-graphs']['in'], 0, -1) . '|cumulative-frequency|measures-of-dispersion/';
        $d['data-and-graphs']['out'] = substr($d['data-and-graphs']['out'], 0, -1) . '|graphs-of-quadratic|trigonometric-graphs/';
        $d['measurement']['in'] = substr($d['measurement']['in'], 0, -1) . '|longitude-and-latitude/';
        $d['measurement']['out'] = substr($d['measurement']['out'], 0, -1) . '|measures-of-dispersion/';
        $d['circles']['in'] = substr($d['circles']['in'], 0, -1) . '|chords-and-tangents/';
        $d['calculus']['in'] = substr($d['calculus']['in'], 0, -1) . '|^integration$/';
        $d['number-bases'] = array('name' => 'Number Bases', 'in' => '/number-bases|binary-numbers/', 'out' => '/^$/',
            'blurb' => 'Binary numbers and other bases: place values, changing to and from base ten, and adding, subtracting and multiplying in other bases.');
    }
    if ($country === 'uk') {
        // A level (Year 12 and 13): calculus, the binomial and normal distributions, partial fractions, mechanics
        $d['calculus']['name'] = 'Calculus';
        $d['calculus']['blurb'] = 'Differentiation, tangents and stationary points, the chain rule, integration techniques, areas under curves, numerical methods and differential equations.';
        $d['calculus']['in'] = substr($d['calculus']['in'], 0, -1) . '|^integration|numerical-methods|differential-equations/';
        $d['probability']['in'] = substr($d['probability']['in'], 0, -1) . '|binomial-distribution|normal-distribution/';
        $d['data-and-graphs']['out'] = substr($d['data-and-graphs']['out'], 0, -1) . '|binomial-distribution|normal-distribution/';
        $d['fractions']['out'] = substr($d['fractions']['out'], 0, -1) . '|partial-fractions/';
        $d['algebra']['in'] = substr($d['algebra']['in'], 0, -1) . '|partial-fractions/';
        // GCSE histograms, iteration and algebraic proof; A level proof, the product and quotient rules and hypothesis tests
        $d['data-and-graphs']['in'] = substr($d['data-and-graphs']['in'], 0, -1) . '|^histograms$/';
        $d['data-and-graphs']['out'] = substr($d['data-and-graphs']['out'], 0, -1) . '|velocity-time/';
        $d['time']['out'] = substr($d['time']['out'], 0, -1) . '|velocity-time/';
        $d['algebra']['in'] = substr($d['algebra']['in'], 0, -1) . '|^iteration$|^proof$/';
        $d['calculus']['in'] = substr($d['calculus']['in'], 0, -1) . '|product-and-quotient-rules/';
        $d['probability']['in'] = substr($d['probability']['in'], 0, -1) . '|hypothesis-testing/';
        $d['mechanics'] = array('name' => 'Mechanics', 'in' => '/kinematics|newtons-laws|moments-and-friction|projectiles|velocity-time-graphs/', 'out' => '/^$/',
            'blurb' => 'Constant acceleration and velocity–time graphs, forces and Newton\'s laws, connected particles, moments, friction and inclined planes, and projectiles.');
    }
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
function topic_gb($country) { return in_array($country, array('uk', 'au', 'sg', 'za', 'in', 'ng'), true); }

function topic_name($t, $country) {
    if ($country === 'au' && isset($t['name_au'])) return $t['name_au'];
    if (topic_gb($country) && isset($t['name_gb'])) return $t['name_gb'];
    return $t['name'];
}
function topic_blurb($t, $country) {
    if ($country === 'mx' && isset($t['blurb_mx'])) return $t['blurb_mx'];
    return (topic_gb($country) && isset($t['blurb_gb'])) ? $t['blurb_gb'] : $t['blurb'];
}

/* slugs of the topics a unit belongs to (most specific first: definition order) */
function unit_topic_slugs($unit_slug, $country = null, $subject = null) {
    $out = array();
    foreach (topic_defs($country, $subject) as $k => $t) {
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
    foreach (topic_defs($c, $s) as $k => $t) {
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
    if ($units[0]['country'] === 'tw' || $units[0]['country'] === 'cn') return $first . '到' . $last;
    if ($units[0]['country'] === 'kr') return $first . '~' . $last;
    if ($units[0]['country'] === 'fr') return 'du ' . $first . ' au ' . $last;
    if ($units[0]['country'] === 'br') return 'do ' . $first . ' ao ' . $last;
    if ($units[0]['country'] === 'es' || $units[0]['country'] === 'mx') return 'de ' . $first . ' a ' . $last;
    if ($units[0]['country'] === 'id') return $first . ' sampai ' . $last;
    if ($units[0]['country'] === 'tr') return $first . ' – ' . $last;
    if ($units[0]['country'] === 'se') return $first . '–' . $last;
    if ($units[0]['country'] === 'it') return 'dalla ' . strtolower($first) . ' alla ' . strtolower($last);
    return ($units[0]['country'] === 'de' || $units[0]['country'] === 'ch') ? $first . ' bis ' . $last : $first . ' to ' . $last;
}

/* lower case for use inside a sentence, keeping "2D", "3D" */
function topic_lc($name) {
    return preg_replace_callback('/\b[A-Za-z]+\b/', function ($m) { return strtolower($m[0]); }, $name);
}
