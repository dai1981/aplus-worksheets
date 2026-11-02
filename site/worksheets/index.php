<?php
/* Aplus worksheets: router
   /worksheets/                               -> home (countries)
   /worksheets/us/                            -> country (subjects)
   /worksheets/us/math/                       -> subject (grades)
   /worksheets/us/math/grade-3/               -> grade (skills list)
   /worksheets/us/math/grade-3/area/          -> lesson + 100 questions
   /worksheets/us/math/grade-3/area/print/    -> printable worksheet
   /worksheets/us/math/topics/                -> topic list
   /worksheets/us/math/topics/fractions/      -> every skill on one topic (inc/topics.php)
   /worksheets/us/math/grade-3/area/preview.png -> preview picture (also grade and topic pages)
   /worksheets/sitemap.xml                    -> sitemap
*/
require __DIR__ . '/inc/core.php';

$p = isset($_GET['p']) ? (string)$_GET['p'] : '';
$p = trim($p, '/');

if ($p === 'sitemap.xml') {
    try { require __DIR__ . '/views/sitemap.php'; }
    catch (PDOException $e) { http_response_code(503); }
    exit;
}

// preview image of a skill, grade or topic: .../preview.png
if (preg_match('#^([a-z0-9/-]{1,200})/preview\.png$#', $p, $m)) {
    $pseg = explode('/', $m[1]);
    $ok = (count($pseg) === 4 || count($pseg) === 3);
    foreach ($pseg as $s) { if (!preg_match('/^[a-z0-9-]{1,80}$/', $s)) $ok = false; }
    if (!$ok || (count($pseg) === 3 && $pseg[2] === 'topics')) { http_response_code(404); exit; }
    require __DIR__ . '/inc/preview.php';
    try { preview_route($pseg); }
    catch (PDOException $e) { http_response_code(503); }
    exit;
}

// always end with a slash (one URL per page)
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($p !== '' && substr($uri, -1) !== '/') {
    header('Location: ' . url($p . '/'), true, 301);
    exit;
}

$seg = $p === '' ? array() : explode('/', $p);
foreach ($seg as $s) {
    if (!preg_match('/^[a-z0-9-]{1,80}$/', $s)) not_found();
}

try {
    switch (count($seg)) {
        case 0: require __DIR__ . '/views/home.php'; break;
        case 1: require __DIR__ . '/views/country.php'; break;
        case 2: require __DIR__ . '/views/subject.php'; break;
        case 3:
            if ($seg[2] === 'topics') { require __DIR__ . '/views/topics.php'; break; }
            require __DIR__ . '/views/grade.php'; break;
        case 4:
            if ($seg[2] === 'topics') { require __DIR__ . '/views/topic.php'; break; }
            require __DIR__ . '/views/unit.php'; break;
        case 5:
            if ($seg[4] !== 'print') not_found();
            require __DIR__ . '/views/print.php';
            break;
        default: not_found();
    }
} catch (PDOException $e) {
    http_response_code(503);
    header('Retry-After: 120');
    echo 'Temporarily unavailable. Please try again in a moment.';
}
