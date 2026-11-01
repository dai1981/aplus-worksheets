<?php
$country = get_country($seg[0]);
$subject = $country ? get_subject($seg[0], $seg[1]) : null;
if (!$subject) not_found();
T(array($country['lang']));
$grades = qa('SELECT g.*, (SELECT COUNT(*) FROM ws_unit u WHERE u.country=g.country AND u.subject=g.subject AND u.grade=g.slug) AS n
              FROM ws_grade g WHERE g.country=? AND g.subject=? ORDER BY g.sort', array($seg[0], $seg[1]));
$grades = array_values(array_filter($grades, function ($g) { return $g['n'] > 0; }));   // hide grades with no units yet
$base = $seg[0] . '/' . $seg[1] . '/';
$crumbs = array(array(T('worksheets'), ''), array($country['name'], $seg[0] . '/'),
                array($subject['name'], $base));

page_head(array(
    'lang' => $country['lang'], 'hreflang' => $country['hreflang'],
    'title' => 'Free ' . $subject['name'] . ' Worksheets by Grade (' . $country['standard'] . ') | ' . SITE_NAME,
    'desc' => $subject['intro'],
    'canonical' => $base,
));
site_header($crumbs);
?>
<main class="sn-wrap">
<h1><?= h($subject['name']) ?> Worksheets</h1>
<div class="sx-hero"><p><?= h($subject['intro']) ?></p></div>
<h2><?= h(T('pick_grade')) ?></h2>
<ul class="sx-grades">
<?php foreach ($grades as $g): ?>
  <li><a href="<?= url($base . $g['slug'] . '/') ?>"><?= h($g['name']) ?><span class="n"><?= h(sprintf(T('skills_count'), $g['n'])) ?></span><span class="lv-tile"<?= rank_attrs($seg[0], $seg[1], $g['slug'], list_units($seg[0], $seg[1], $g['slug']), $g['name'] . ' ' . $subject['name'], 'tile') ?>></span></a></li>
<?php endforeach; ?>
</ul>
</main>
<?php
echo breadcrumb_ld($crumbs);
site_footer($country['lang']);
?>
</body>
</html>
