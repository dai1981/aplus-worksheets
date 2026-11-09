<?php
$country = get_country($seg[0]);
$subject = $country ? get_subject($seg[0], $seg[1]) : null;
$grade = $subject ? get_grade($seg[0], $seg[1], $seg[2]) : null;
$u = $grade ? get_unit($seg[0], $seg[1], $seg[2], $seg[3]) : null;
if (!$u) not_found();
T(array($country['lang']));

$gbase = $seg[0] . '/' . $seg[1] . '/' . $seg[2] . '/';
$path = $gbase . $u['slug'] . '/';
$pkey = prog_key($seg[0], $seg[1], $seg[2], $u['slug']);
$sets = json_decode($u['sets_json'], true);
$faq = json_decode($u['faq_json'], true);
if (!$faq) $faq = array();
$siblings = list_units($seg[0], $seg[1], $seg[2]);
$prev = $next = null;
foreach ($siblings as $i => $s) {
    if ($s['slug'] === $u['slug']) {
        if ($i > 0) $prev = $siblings[$i - 1];
        if ($i < count($siblings) - 1) $next = $siblings[$i + 1];
    }
}
$crumbs = array(array(T('worksheets'), ''), array($country['name'], $seg[0] . '/'),
                array($subject['name'], $seg[0] . '/' . $seg[1] . '/'),
                array($grade['name'], $gbase), array($u['short_title'], $path));
require_once __DIR__ . '/../inc/topics.php';
$utopics = array();                              // topic hubs this skill belongs to
$tall = topics_for($seg[0], $seg[1]);
$tdefs = topic_defs();
foreach (unit_topic_slugs($u['slug']) as $tk) {
    if (isset($tall[$tk])) $utopics[$tk] = topic_name($tdefs[$tk], $seg[0]) . ' worksheets: ' . topic_range($tall[$tk]);
}
$JF = JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG;

page_head(array(
    'lang' => $country['lang'], 'hreflang' => $country['hreflang'],
    'title' => $u['seo_title'] . ' | ' . SITE_NAME,
    'desc' => $u['meta_desc'], 'canonical' => $path, 'og_type' => 'article',
    'image' => preview_path($path),
));
site_header($crumbs);
?>
<main class="sn-wrap">
<article>
  <span class="sn-grade"><?= h($grade['name'] . ' ' . $subject['name'] . ' · ' . $u['domain']) ?></span>
  <h1><?= h($u['title']) ?></h1>

  <div class="qz-hook" data-k="<?= h($pkey) ?>" data-n="<?= count($sets) ?>">
    <div class="qz-hook-h"><?= h(T('hook_title')) ?> <small><?= h(T('hook_sub')) ?></small></div>
    <div class="sp-bar" data-prog="<?= h($pkey) ?>" data-sets="<?= count($sets) ?>"></div>
    <p class="qz-hook-m"></p>
    <a class="qz-hook-go" href="#quiz"><?= h(T('hook_go')) ?><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v15M5 12l7 7 7-7"/></svg></a>
  </div>

  <a class="lv-mini" href="<?= url($gbase) ?>"<?= rank_attrs($seg[0], $seg[1], $seg[2], $siblings, $grade['name'] . ' ' . $subject['name'], 'mini') ?>></a>

  <div class="sn-key">
    <div class="sn-key-h"><?= h(T('points')) ?></div>
    <div class="sn-key-b"><span class="big"><?= h($u['key_big']) ?></span>
    <p class="sub"><?= h($u['key_sub']) ?></p></div>
  </div>
  <p class="ws-share"><?= pin_link($path, 'Free ' . $grade['name'] . ' ' . strtolower($subject['name']) . ' ' . strtolower($u['short_title']) . ' worksheet: short lesson, 100 practice questions and a printable answer key.') ?></p>

  <?php if ($u['standard_code']): ?>
  <p class="ws-std"><span><?= h($country['standard']) ?></span>
    <?php if ($u['standard_url']): ?><a href="<?= h($u['standard_url']) ?>" rel="noopener" target="_blank"><?= h($u['standard_code']) ?></a><?php else: ?><b><?= h($u['standard_code']) ?></b><?php endif; ?>
    <?= h($u['standard_text']) ?></p>
  <?php endif; ?>

  <?= $u['body_html'] /* trusted: written by us in content/*.json */ ?>

  <h2 id="quiz"><?= h(T('quiz100')) ?></h2>
  <p><?= h(T('quiz_lead')) ?></p>
  <div class="sp-wrap"><div class="h"><span><?= h(T('your_score')) ?></span></div>
    <div class="sp-bar" data-prog="<?= h($pkey) ?>" data-sets="<?= count($sets) ?>"></div></div>
<?php foreach ($sets as $i => $s): $n = $i + 1; ?>
  <h3><?= $n ?>. <?= h($s['title']) ?></h3>
  <div class="sn-quiz" data-quiz="s<?= $n ?>"></div>
  <script type="application/json" data-quiz-for="s<?= $n ?>"><?= json_encode(array('title' => $s['title'], 'key' => $pkey . '-' . $n, 'grade' => prog_key($seg[0], $seg[1], $seg[2]), 'items' => $s['items']), $JF) ?></script>
<?php endforeach; ?>

<?php if ($faq): ?>
  <section class="sn-faq">
  <h2><?= h(T('faq')) ?></h2>
<?php foreach ($faq as $f): ?>
    <details><summary><?= h($f['q']) ?></summary><div class="sn-a"><?= h($f['a']) ?></div></details>
<?php endforeach; ?>
  </section>
<?php endif; ?>

  <p class="sn-byline sn-byline-b"><?= h(T('by')) ?> <?= h(SITE_NAME) ?> | <?= h(T('updated')) ?> <time datetime="<?= h($u['updated']) ?>"><?= h(date('F j, Y', strtotime($u['updated']))) ?></time></p>
</article>

<nav class="sn-related">
  <h2><?= h(T('related')) ?></h2>
  <?php if ($prev || $next): ?>
  <div class="sn-pn">
    <?php if ($prev): ?><a href="<?= url($gbase . $prev['slug'] . '/') ?>"><small><?= h(T('prev')) ?></small><?= h($prev['short_title']) ?></a><?php endif; ?>
    <?php if ($next): ?><a class="sn-nx" href="<?= url($gbase . $next['slug'] . '/') ?>"><small><?= h(T('next_u')) ?></small><?= h($next['short_title']) ?></a><?php endif; ?>
  </div>
  <?php endif; ?>
  <ul class="sn-links">
    <li><a href="<?= url($path . 'print/') ?>"><?= h(T('printable_of')) ?></a></li>
    <li><a href="<?= url($gbase) ?>"><?= h(T('all_units')) ?> <?= h($grade['name'] . ' ' . $subject['name']) ?></a></li>
<?php foreach ($utopics as $tk => $tn): ?>
    <li><a href="<?= url($seg[0] . '/' . $seg[1] . '/topics/' . $tk . '/') ?>"><?= h($tn) ?></a></li>
<?php endforeach; ?>
  </ul>
  <h3><?= h($grade['name'] . ' ' . $subject['name']) ?></h3>
  <ul class="sn-links">
<?php foreach ($siblings as $s): ?>
    <li><a href="<?= url($gbase . $s['slug'] . '/') ?>"<?= $s['slug'] === $u['slug'] ? ' aria-current="page"' : '' ?>><?= h($s['title']) ?></a></li>
<?php endforeach; ?>
  </ul>
</nav>
</main>
<?php
echo breadcrumb_ld($crumbs);
$lr = array('@context' => 'https://schema.org', '@type' => 'LearningResource',
    'name' => $u['title'], 'description' => $u['meta_desc'], 'url' => abs_url($path),
    'inLanguage' => $country['hreflang'], 'isAccessibleForFree' => true,
    'learningResourceType' => array('Lesson', 'Practice problems', 'Worksheet'),
    'educationalLevel' => $grade['name'],
    'about' => array('@type' => 'Thing', 'name' => $subject['name']),
    'author' => array('@type' => 'Organization', 'name' => SITE_NAME),
    'publisher' => array('@type' => 'Organization', 'name' => SITE_NAME, 'url' => SITE_HOME),
    'dateModified' => $u['updated']);
if (preview_path($path)) $lr['image'] = abs_url(preview_path($path));
// what the page teaches, who it is for (helps search engines and AI answers)
$lr['about'] = array(array('@type' => 'Thing', 'name' => $u['short_title']), array('@type' => 'Thing', 'name' => $subject['name']));
if ($u['key_big']) $lr['teaches'] = $u['key_big'];
$lr['audience'] = array('@type' => 'EducationalAudience', 'educationalRole' => array('student', 'teacher', 'parent'));
if (preg_match('/^grade-(\d+)$/', $grade['slug'], $gm) && ($country['code'] === 'us' || strpos($country['code'], 'ca') === 0)) {   // Canada: Grade 3 = age 8-9, like the US
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);
} elseif (preg_match('/^year-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'uk') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 4) . '-' . ((int)$gm[1] + 5);   // England: Year 4 = age 8-9
} elseif (preg_match('/^year-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'au') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Australia: Year 3 = age 8-9
} elseif (preg_match('/^primary-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'sg') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Singapore: Primary 4 = age 9-10
}
if ($u['standard_code']) {
    $al = array('@type' => 'AlignmentObject', 'alignmentType' => 'teaches',
                'educationalFramework' => $country['standard'], 'targetName' => $u['standard_code'],
                'targetDescription' => $u['standard_text']);
    if ($u['standard_url']) $al['targetUrl'] = $u['standard_url'];
    $lr['educationalAlignment'] = $al;
}
echo jsonld($lr);
if ($faq) {
    $qs = array();
    foreach ($faq as $f) {
        $qs[] = array('@type' => 'Question', 'name' => $f['q'],
                      'acceptedAnswer' => array('@type' => 'Answer', 'text' => $f['a']));
    }
    echo jsonld(array('@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $qs));
}
site_footer($country['lang']);
?>
</body>
</html>
