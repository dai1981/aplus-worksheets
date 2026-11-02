<?php
/* /worksheets/sitemap.xml : every page, built from the database */
header('Content-Type: application/xml; charset=UTF-8');
header('Cache-Control: public, max-age=3600');

$urls = array(array('', null));
foreach (qa('SELECT code FROM ws_country ORDER BY sort') as $c) $urls[] = array($c['code'] . '/', null);
foreach (qa('SELECT country, slug FROM ws_subject ORDER BY sort') as $s) $urls[] = array($s['country'] . '/' . $s['slug'] . '/', null);
foreach (qa('SELECT g.country, g.subject, g.slug, (SELECT MAX(u.updated) FROM ws_unit u WHERE u.country=g.country AND u.subject=g.subject AND u.grade=g.slug) AS up FROM ws_grade g ORDER BY g.sort') as $g) {
    if ($g['up'] === null) continue;            // no units yet
    $urls[] = array($g['country'] . '/' . $g['subject'] . '/' . $g['slug'] . '/', $g['up']);
}
require_once __DIR__ . '/../inc/topics.php';
foreach (qa('SELECT country, slug FROM ws_subject ORDER BY sort') as $s) {
    $tp = topics_for($s['country'], $s['slug']);
    if (!$tp) continue;
    $urls[] = array($s['country'] . '/' . $s['slug'] . '/topics/', null);
    foreach ($tp as $k => $list) {
        $up = null;
        foreach ($list as $x) { if ($up === null || $x['updated'] > $up) $up = $x['updated']; }
        $urls[] = array($s['country'] . '/' . $s['slug'] . '/topics/' . $k . '/', $up);
    }
}
foreach (qa('SELECT country, subject, grade, slug, updated FROM ws_unit ORDER BY country, subject, grade, sort') as $u) {
    $p = $u['country'] . '/' . $u['subject'] . '/' . $u['grade'] . '/' . $u['slug'] . '/';
    $urls[] = array($p, $u['updated'], preview_path($p));
    $urls[] = array($p . 'print/', $u['updated']);
}

echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
foreach ($urls as $x) {
    echo '<url><loc>' . h(abs_url($x[0])) . '</loc>' . ($x[1] ? '<lastmod>' . h($x[1]) . '</lastmod>' : '')
       . (!empty($x[2]) ? '<image:image><image:loc>' . h(abs_url($x[2])) . '</image:loc></image:image>' : '') . "</url>\n";
}
echo "</urlset>\n";
