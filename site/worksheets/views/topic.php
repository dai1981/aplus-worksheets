<?php
/* /worksheets/{country}/{subject}/topics/{topic}/ : every skill on one topic, lowest grade first */
require_once __DIR__ . '/../inc/topics.php';
$country = get_country($seg[0]);
$subject = $country ? get_subject($seg[0], $seg[1]) : null;
if (!$subject) not_found();
T(array($country['lang']));
$defs = topic_defs();
$all = topics_for($seg[0], $seg[1]);
if (!isset($all[$seg[3]])) not_found();
$tk = $seg[3];
$units = $all[$tk];
$name = topic_name($defs[$tk], $seg[0]);
$lc = topic_lc($name);
$range = topic_range($units);
$sbase = $seg[0] . '/' . $seg[1] . '/';
$path = $sbase . 'topics/' . $tk . '/';
$paper = $country['paper'] === 'letter' ? 'Letter' : 'A4';
$crumbs = array(array(T('worksheets'), ''), array($country['name'], $seg[0] . '/'),
                array($subject['name'], $sbase), array($name, $path));

$groups = array();
foreach ($units as $u) $groups[$u['grade']][] = $u;
$gnames = array();
foreach ($units as $u) $gnames[$u['grade']] = $u['grade_name'];
$titles = array();
foreach ($units as $u) $titles[] = $u['short_title'];
$first = $units[0]; $last = $units[count($units) - 1];

$faq = array(
    array('q' => 'What ' . $lc . ' worksheets are on this page?',
          'a' => 'There are ' . count($units) . ' ' . $lc . ' skills from ' . $range . ': '
               . implode(', ', array_slice($titles, 0, 6)) . (count($titles) > 6 ? ', and more' : '') . '.'),
    array('q' => 'When do students learn ' . $lc . ' in the ' . $country['standard'] . '?',
          'a' => $name . ' starts in ' . $first['grade_name'] . ' with ' . $first['short_title']
               . ($first['grade'] === $last['grade'] ? '.' : ' and goes up to ' . $last['grade_name'] . ' with ' . $last['short_title'] . '.')),
    array('q' => 'How should my child use these ' . $lc . ' worksheets?',
          'a' => 'Pick the skill for their ' . strtolower(rtrim(T('grades'), 's')) . ', read the short lesson, then do the 5 practice sets of 20 questions. '
               . 'Each answer is checked right away. Print the ' . $paper . ' worksheet for extra practice; the answer key is on the last page.'),
    array('q' => 'Are these ' . $lc . ' worksheets free?',
          'a' => 'Yes. The lessons, the online practice and the printable worksheets with answer keys are free for home and classroom use. No sign-up is needed.'),
);

page_head(array(
    'lang' => $country['lang'], 'hreflang' => $country['hreflang'],
    'title' => $name . ' Worksheets: Free ' . $range . ' ' . $subject['name'] . ' Practice with Answers | ' . SITE_NAME,
    'desc' => 'Free ' . $lc . ' worksheets for ' . $range . ', aligned to the ' . $country['standard'] . ': '
              . count($units) . ' skills, each with a lesson, 100 practice questions and a printable answer key.',
    'canonical' => $path, 'image' => preview_path($path),
));
site_header($crumbs);
?>
<main class="sn-wrap">
<span class="sn-grade"><?= h($range . ' · ' . $country['standard']) ?></span>
<h1><?= h($name) ?> Worksheets</h1>
<div class="sx-hero"><p><?= h(topic_blurb($defs[$tk], $seg[0])) ?> Every skill below has a short lesson, 100 practice questions with instant feedback and a printable <?= h($paper) ?> worksheet with an answer key. Free, no sign-up.</p></div>

<?php if (count($groups) > 1): ?>
<ul class="tp-grades" aria-label="<?= h(T('grades')) ?>">
<?php foreach ($groups as $g => $list): ?>
  <li><a href="#<?= h($g) ?>"><?= h($gnames[$g]) ?></a></li>
<?php endforeach; ?>
</ul>
<?php endif; ?>

<?php foreach ($groups as $g => $list): $gbase = $sbase . $g . '/'; ?>
<h2 id="<?= h($g) ?>"><?= h($gnames[$g] . ' ' . $name) ?></h2>
<ul class="sx-list">
<?php foreach ($list as $u): $up = $gbase . $u['slug'] . '/'; ?>
<li><div class="m"><span class="t"><?= h($u['title']) ?></span>
  <span class="d"><?= h($u['standard_code']) ?> · 100 <?= h(T('questions')) ?></span>
  <?php if ($u['key_big']): ?><span class="k"><?= h($u['key_big']) ?></span><?php endif; ?>
  <span class="sp-bar" data-prog="<?= h(prog_key($seg[0], $seg[1], $g, $u['slug'])) ?>" data-sets="5"></span></div>
  <p class="act"><a class="q" href="<?= url($up) ?>"><?= h(T('learn_quiz')) ?></a><a href="<?= url($up . 'print/') ?>"><?= h(T('print')) ?></a><a href="<?= url($gbase) ?>"><?= h($gnames[$g]) ?></a></p></li>
<?php endforeach; ?>
</ul>
<?php endforeach; ?>

<section class="sn-faq">
<h2><?= h(T('faq')) ?></h2>
<?php foreach ($faq as $f): ?>
  <details><summary><?= h($f['q']) ?></summary><div class="sn-a"><?= h($f['a']) ?></div></details>
<?php endforeach; ?>
</section>

<h2>More <?= h(strtolower($subject['name'])) ?> topics</h2>
<ul class="tp-chips">
<?php foreach ($all as $ok => $ou): if ($ok === $tk) continue; ?>
  <li><a href="<?= url($sbase . 'topics/' . $ok . '/') ?>"><?= h(topic_name($defs[$ok], $seg[0])) ?><span class="n"><?= count($ou) ?></span></a></li>
<?php endforeach; ?>
</ul>
</main>
<?php
echo breadcrumb_ld($crumbs);
$items = array();
foreach ($units as $i => $u) {
    $items[] = array('@type' => 'ListItem', 'position' => $i + 1, 'name' => $u['grade_name'] . ': ' . $u['title'],
                     'url' => abs_url($sbase . $u['grade'] . '/' . $u['slug'] . '/'));
}
$cp = array('@context' => 'https://schema.org', '@type' => 'CollectionPage',
    'name' => $name . ' Worksheets', 'description' => topic_blurb($defs[$tk], $seg[0]), 'url' => abs_url($path),
    'inLanguage' => $country['hreflang'], 'isAccessibleForFree' => true,
    'about' => array('@type' => 'Thing', 'name' => $name),
    'mainEntity' => array('@type' => 'ItemList', 'numberOfItems' => count($items), 'itemListElement' => $items));
if (preview_path($path)) $cp['image'] = abs_url(preview_path($path));
echo jsonld($cp);
$qs = array();
foreach ($faq as $f) $qs[] = array('@type' => 'Question', 'name' => $f['q'], 'acceptedAnswer' => array('@type' => 'Answer', 'text' => $f['a']));
echo jsonld(array('@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $qs));
site_footer($country['lang']);
?>
</body>
</html>
