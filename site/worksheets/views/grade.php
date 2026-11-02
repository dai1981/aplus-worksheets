<?php
$country = get_country($seg[0]);
$subject = $country ? get_subject($seg[0], $seg[1]) : null;
$grade = $subject ? get_grade($seg[0], $seg[1], $seg[2]) : null;
if (!$grade) not_found();
T(array($country['lang']));
$units = list_units($seg[0], $seg[1], $seg[2]);
if (!$units) not_found();                       // a grade with no units yet is not shown
$base = $seg[0] . '/' . $seg[1] . '/' . $seg[2] . '/';
$gkey = prog_key($seg[0], $seg[1], $seg[2]);
$crumbs = array(array(T('worksheets'), ''), array($country['name'], $seg[0] . '/'),
                array($subject['name'], $seg[0] . '/' . $seg[1] . '/'),
                array($grade['name'], $base));

// group by domain, keep order
$groups = array();
foreach ($units as $u) { $groups[$u['domain']][] = $u; }
$keys = array();
foreach ($units as $u) { $keys[] = prog_key($seg[0], $seg[1], $seg[2], $u['slug']); }
$names = array();
foreach ($units as $u) { $names[] = $u['short_title']; }

page_head(array(
    'lang' => $country['lang'], 'hreflang' => $country['hreflang'],
    'title' => sprintf(T('grade_ws'), $grade['name'], $subject['name']) . ': Free Printable + Online Practice | ' . SITE_NAME,
    'desc' => 'Free ' . $grade['name'] . ' ' . strtolower($subject['name']) . ' worksheets aligned to the '
              . $country['standard'] . ': ' . implode(', ', array_slice($names, 0, 6))
              . '. 100 practice questions per skill and printable answer keys.',
    'canonical' => $base, 'image' => preview_path($base),
));
site_header($crumbs);
?>
<main class="sn-wrap">
<h1><?= h($grade['name'] . ' ' . $subject['name']) ?> Worksheets</h1>
<div class="sx-hero"><p><?= h($grade['intro']) ?></p></div>

<section class="lv" aria-label="Rank"<?= rank_attrs($seg[0], $seg[1], $seg[2], $units, $grade['name'] . ' ' . $subject['name'], 'card') ?>></section>

<?php foreach ($groups as $domain => $list): ?>
<h2><?= h($domain) ?></h2>
<ul class="sx-list">
<?php foreach ($list as $u): $up = $base . $u['slug'] . '/'; ?>
<li><div class="m"><span class="t"><?= h($u['title']) ?></span>
  <span class="d"><?= h($u['standard_code']) ?> · 100 <?= h(T('questions')) ?></span>
  <span class="sp-bar" data-prog="<?= h(prog_key($seg[0], $seg[1], $seg[2], $u['slug'])) ?>" data-sets="5"></span></div>
  <p class="act"><a class="q" href="<?= url($up) ?>"><?= h(T('learn_quiz')) ?></a><a href="<?= url($up . 'print/') ?>"><?= h(T('print')) ?></a><?php if ($u['pdf_url']): ?><a class="f" href="<?= h($u['pdf_url']) ?>" download><?= h(T('pdf')) ?></a><?php endif; ?></p></li>
<?php endforeach; ?>
</ul>
<?php endforeach; ?>

<p class="lv-clear"><button type="button" class="sp-clear" data-prog-clear="<?= h($gkey) ?>"><span class="sp-clear-t"><?= h(T('clear_grade')) ?></span></button></p>

<?php
require_once __DIR__ . '/../inc/topics.php';
$gtopics = array(); $tdefs = topic_defs();
foreach (topics_for($seg[0], $seg[1]) as $tk => $tu) {
    foreach ($tu as $x) { if ($x['grade'] === $seg[2]) { $gtopics[$tk] = topic_name($tdefs[$tk], $seg[0]); break; } }
}
if ($gtopics): ?>
<h2 id="topics">Topics across all <?= h(strtolower(T('grades'))) ?></h2>
<ul class="tp-chips">
<?php foreach ($gtopics as $tk => $tn): ?>
  <li><a href="<?= url($seg[0] . '/' . $seg[1] . '/topics/' . $tk . '/') ?>"><?= h($tn) ?></a></li>
<?php endforeach; ?>
</ul>
<?php endif; ?>

<h2 id="print"><?= h(T('print_sheets')) ?></h2>
<div class="sx-hero"><p><?= h(T('print_note')) ?>. <?= h(T('license')) ?></p></div>
<ul class="pg">
<?php foreach ($units as $u): ?>
  <li><a href="<?= url($base . $u['slug'] . '/print/') ?>"><span class="pg-doc" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span class="t"><?= h($u['short_title']) ?></span><span class="d"><?= h($u['standard_code']) ?></span><span class="f"><?= h(strtoupper($country['paper'])) ?> · 4 pages</span></a></li>
<?php endforeach; ?>
</ul>
</main>
<?php
echo breadcrumb_ld($crumbs);
$items = array();
foreach ($units as $i => $u) {
    $items[] = array('@type' => 'ListItem', 'position' => $i + 1, 'name' => $u['title'],
                     'url' => abs_url($base . $u['slug'] . '/'));
}
echo jsonld(array('@context' => 'https://schema.org', '@type' => 'CollectionPage',
    'name' => $grade['name'] . ' ' . $subject['name'] . ' Worksheets', 'url' => abs_url($base),
    'inLanguage' => $country['hreflang'],
    'mainEntity' => array('@type' => 'ItemList', 'itemListElement' => $items)));
site_footer($country['lang']);
?>
</body>
</html>
