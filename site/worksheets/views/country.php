<?php
$country = get_country($seg[0]);
if (!$country) not_found();
T(array($country['lang']));
$subjects = qa('SELECT * FROM ws_subject WHERE country=? ORDER BY sort, name', array($country['code']));
$base = $country['code'] . '/';
$stds = array();
foreach ($subjects as $s) $stds[subject_standard($country, $s['slug'])] = 1;   // math and science can follow different standards
$crumbs = array(array(T('worksheets'), ''), array($country['name'], $base));

page_head(array(
    'lang' => $country['lang'], 'hreflang' => $country['hreflang'],
    'title' => sprintf(T('country_title'), $country['name'], implode(', ', array_keys($stds))) . ' | ' . SITE_NAME,
    'desc' => $country['intro'],
    'canonical' => $base,
));
site_header($crumbs);
?>
<main class="sn-wrap">
<h1><?= h(sprintf(T('country_h1'), $country['name'])) ?></h1>
<div class="sx-hero"><p><?= h($country['intro']) ?></p></div>
<h2><?= h(T('pick_subject')) ?></h2>
<ul class="sx-grades">
<?php foreach ($subjects as $s): ?>
  <li><a href="<?= url($base . $s['slug'] . '/') ?>"><?= h($s['name']) ?><span class="n"><?= h(subject_standard($country, $s['slug'])) ?></span></a></li>
<?php endforeach; ?>
</ul>
</main>
<?php
echo breadcrumb_ld($crumbs);
site_footer($country['lang'], false);
?>
</body>
</html>
