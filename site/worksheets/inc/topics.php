<?php
/* Topic hubs: /worksheets/{country}/{subject}/topics/{topic}/
   One page per topic that collects every skill on that topic, from the lowest grade to the highest.
   Units join a topic when their slug matches 'in' and does not match 'out'.
   Nothing here is stored in the database: the list is built from ws_unit on each request. */

function topic_defs() {
    return array(
        'fractions' => array('name' => 'Fractions',
            'in' => '/fraction|halves|thirds|fourths|quarters|mixed-num|improper|fair-shares|partition-shapes|operations-with-rational/',
            'out' => '/decimals-tenths/',
            'blurb' => 'Start with halves and quarters, then move on to equivalent fractions, comparing fractions, mixed numbers, and adding, subtracting, multiplying and dividing fractions.'),
        'decimals' => array('name' => 'Decimals',
            'in' => '/decimal|thousandths/', 'out' => '/^$/',
            'blurb' => 'Tenths and hundredths first, then place value, comparing and rounding decimals, and adding, subtracting, multiplying and dividing with decimals.'),
        'percents' => array('name' => 'Percents', 'name_gb' => 'Percentages',
            'in' => '/percent|discount/', 'out' => '/^$/',
            'blurb' => 'What percent means, converting between fractions, decimals and percents, finding a percent of an amount, discounts and percent change.',
            'blurb_gb' => 'What percentage means, converting between fractions, decimals and percentages, finding a percentage of an amount, discounts and percentage change.'),
        'ratios-and-rates' => array('name' => 'Ratios and Rates',
            'in' => '/(^|-)ratios?(-|$)|(^|-)rates?(-|$)|proportion|scaling/', 'out' => '/^$/',
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
            'in' => '/add|subtract|number-bonds|make-10|ten-more|change-in-quantity|word-problems/',
            'out' => '/fraction|decimal|integer|polynomial|mixed-num|multiplicative|ratio/',
            'blurb' => 'Number bonds and facts to 20, mental strategies, adding and subtracting with regrouping, and multi-step word problems.',
            'blurb_gb' => 'Number bonds and facts to 20, mental strategies, column addition and subtraction, and multi-step word problems.'),
        'place-value' => array('name' => 'Place Value and Numbers',
            'in' => '/place-value|numbers-to|(^|-)count|tens-and-ones|compare-t|roman|large-numbers|billions|ordinal|odd-and-even|skip-counting|powers-and-large/',
            'out' => '/money|fraction/',
            'blurb' => 'Counting, tens and ones, place value to millions and beyond, comparing and ordering numbers, and odd and even numbers.'),
        'rounding-and-estimation' => array('name' => 'Rounding and Estimation',
            'in' => '/round|estimat|benchmark/', 'out' => '/^$/',
            'blurb' => 'Rounding to the nearest 10, 100 and 1000, rounding decimals, and estimating to check answers.'),
        'order-of-operations' => array('name' => 'Order of Operations',
            'in' => '/order-of-operations|numerical-expressions/', 'out' => '/^$/',
            'blurb' => 'Which operation comes first, working with brackets and exponents, and writing number problems as one expression.'),
        'factors-and-multiples' => array('name' => 'Factors, Multiples and Primes',
            'in' => '/factor|prime|gcf|multiples|divisib/', 'out' => '/multiples-of-10/',
            'blurb' => 'Factors and multiples, prime and composite numbers, common factors and common multiples.'),
        'exponents-and-roots' => array('name' => 'Exponents and Square Roots',
            'in' => '/exponent|square-root|squares-cubes|perfect-square|cube-root|scientific|powers|square-numbers/', 'out' => '/powers-of-10/',
            'blurb' => 'Powers and exponents, perfect squares, square roots and cube roots, and scientific notation.'),
        'integers' => array('name' => 'Integers and Negative Numbers',
            'in' => '/integer|negative|absolute|rational-numbers/', 'out' => '/^$/',
            'blurb' => 'Negative numbers on the number line, comparing integers, absolute value, and adding, subtracting, multiplying and dividing integers.'),
        'algebra' => array('name' => 'Algebra, Equations and Patterns',
            'in' => '/pattern|algebra|expression|equation|inequalit|equal-sign|equality|equal-and-not|number-sentences|relation|polynomial|missing-numbers/',
            'out' => '/order-of-operations-and|angle-relationships/',
            'blurb' => 'Number and shape patterns, the equal sign, missing numbers, expressions, one- and two-step equations, inequalities and linear relations.'),
        'money' => array('name' => 'Money and Financial Literacy',
            'in' => '/money|coins|financial|budget|best-buys|interest|exchange|discount-gst/', 'out' => '/^$/',
            'blurb' => 'Counting coins and bills, making change, budgets, discounts and tax, saving and interest.',
            'blurb_gb' => 'Counting coins and notes, giving change, budgets, discounts, saving and interest.'),
        'time' => array('name' => 'Time',
            'in' => '/time|clock|calendar|days-weeks|timetables|duration|elapsed/', 'out' => '/times-table/',
            'blurb' => 'Telling time on analog and digital clocks, a.m. and p.m., the 24-hour clock, elapsed time and calendars.',
            'blurb_gb' => 'Telling the time on analogue and digital clocks, the 12- and 24-hour clock, how long things take, and calendars.'),
        'measurement' => array('name' => 'Measurement',
            'in' => '/measur|length|mass|capacity|metric|convert|scales|conversion/', 'out' => '/angle/',
            'blurb' => 'Measuring length, mass and capacity, reading scales, and converting between units.'),
        'area-and-perimeter' => array('name' => 'Area and Perimeter',
            'in' => '/area|perimeter/', 'out' => '/surface-area-nets/',
            'blurb' => 'Perimeter by counting and by adding sides, area of rectangles, triangles and other polygons, and area of circles.'),
        'volume' => array('name' => 'Volume and Surface Area',
            'in' => '/volume|surface-area/', 'out' => '/^$/',
            'blurb' => 'Volume by counting cubes, volume of cubes, cuboids, prisms and cylinders, capacity, and surface area from nets.'),
        'angles' => array('name' => 'Angles',
            'in' => '/(^|-)angles?(-|$)|turns/', 'out' => '/^$/',
            'blurb' => 'Right, acute and obtuse angles, measuring with a protractor, angles on a line and at a point, and angles in shapes.'),
        'shapes' => array('name' => '2D and 3D Shapes',
            'in' => '/shape|polygon|quadrilateral|triangle|circles|circumference|prism|3d|2d|nets|objects|parallelogram|rectangles-and-squares|lines-angles|perpendicular|congruence|classify-two|pythagor/',
            'out' => '/circle-graph|number-shape|composite-area|similar-shapes|area-of/',
            'blurb' => 'Naming and sorting 2D shapes and 3D objects, sides and vertices, triangles and quadrilaterals, circles, nets and solids.'),
        'symmetry-and-transformations' => array('name' => 'Symmetry and Transformations',
            'in' => '/symmetr|transform|reflection|translation|tessellation|scale-|similar/', 'out' => '/^$/',
            'blurb' => 'Lines of symmetry, slides, flips and turns, combining transformations, tessellations and scale drawings.'),
        'coordinates-and-position' => array('name' => 'Coordinates and Position',
            'in' => '/coordinat|cartesian|position|direction|maps|location|grid-ref/', 'out' => '/^$/',
            'blurb' => 'Position and direction words, maps and grid references, plotting points and the coordinate plane.'),
        'data-and-graphs' => array('name' => 'Data and Graphs',
            'in' => '/graph|chart|data|plot|tally|pictogra|mean|median|average|statistic|central-tendency|sorting|organize/', 'out' => '/^$/',
            'blurb' => 'Tally charts, picture graphs and bar graphs, line plots and line graphs, pie charts, and the mean, median and mode.',
            'blurb_gb' => 'Tally charts, pictograms and bar charts, line graphs and pie charts, and the mean.'),
        'probability' => array('name' => 'Probability',  'name_au' => 'Chance and Probability',
            'in' => '/probab|chance|likelihood/', 'out' => '/^$/',
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
function unit_topic_slugs($unit_slug) {
    $out = array();
    foreach (topic_defs() as $k => $t) {
        if (preg_match($t['in'], $unit_slug) && !preg_match($t['out'], $unit_slug)) $out[] = $k;
    }
    return $out;
}

/* all units of a country+subject with grade name and order (one query per page) */
function subject_units($c, $s) {
    static $cache = array();
    if (!isset($cache[$c . '/' . $s])) {
        $cache[$c . '/' . $s] = qa('SELECT u.slug, u.title, u.short_title, u.standard_code, u.key_big, u.updated, u.grade,
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
    foreach (topic_defs() as $k => $t) {
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
    return $first === $last ? $first : $first . ' to ' . $last;
}

/* lower case for use inside a sentence, keeping "2D", "3D" */
function topic_lc($name) {
    return preg_replace_callback('/\b[A-Za-z]+\b/', function ($m) { return strtolower($m[0]); }, $name);
}
