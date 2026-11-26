<?php
$country = get_country($seg[0]);
$subject = $country ? get_subject($seg[0], $seg[1]) : null;
$grade = $subject ? get_grade($seg[0], $seg[1], $seg[2]) : null;
$u = $grade ? get_unit($seg[0], $seg[1], $seg[2], $seg[3]) : null;
if (!$u) not_found();
T(array($country['lang']));
$std_name = ($country['code'] === 'it' && substr($grade['slug'], -6) === '-liceo') ? 'Indicazioni nazionali per i licei' : grade_standard($country, $grade);   // Italy: the licei have their own Indicazioni (DM 211/2010)

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
$tdefs = topic_defs($seg[0]);
foreach (unit_topic_slugs($u['slug'], $seg[0]) as $tk) {
    if (isset($tall[$tk])) $utopics[$tk] = sprintf(T('topic_ws'), topic_name($tdefs[$tk], $seg[0]), topic_range($tall[$tk]));
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
  <span class="sn-grade"><?= h(gs($grade['name'], $subject['name']) . ' · ' . $u['domain']) ?></span>
  <h1><?= h($u['title']) ?></h1>

  <div class="qz-hook" data-k="<?= h($pkey) ?>" data-n="<?= count($sets) ?>">
    <div class="qz-hook-h"><?= h(T('hook_title')) ?> <small><?= h(T('hook_sub')) ?></small></div>
    <div class="sp-bar" data-prog="<?= h($pkey) ?>" data-sets="<?= count($sets) ?>"></div>
    <p class="qz-hook-m"></p>
    <a class="qz-hook-go" href="#quiz"><?= h(T('hook_go')) ?><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v15M5 12l7 7 7-7"/></svg></a>
  </div>

  <a class="lv-mini" href="<?= url($gbase) ?>"<?= rank_attrs($seg[0], $seg[1], $seg[2], $siblings, gs($grade['name'], $subject['name']), 'mini') ?>></a>

  <div class="sn-key">
    <div class="sn-key-h"><?= h(T('points')) ?></div>
    <div class="sn-key-b"><span class="big"><?= h($u['key_big']) ?></span>
    <p class="sub"><?= h($u['key_sub']) ?></p></div>
  </div>
  <p class="ws-share"><?= pin_link($path, sprintf(T('pin_unit'), $grade['name'], lc($subject['name']), lc($u['short_title']))) ?></p>


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

  <?php if ($u['standard_code']): ?>
  <p class="ws-std"><span><?= h($std_name) ?></span>
    <?php if ($u['standard_url']): ?><a href="<?= h($u['standard_url']) ?>" rel="noopener" target="_blank"><?= h($u['standard_code']) ?></a><?php else: ?><b><?= h($u['standard_code']) ?></b><?php endif; ?>
    <?= h($u['standard_text']) ?></p>
  <?php endif; ?>

<?php if ($faq): ?>
  <section class="sn-faq">
  <h2><?= h(T('faq')) ?></h2>
<?php foreach ($faq as $f): ?>
    <details><summary><?= h($f['q']) ?></summary><div class="sn-a"><?= h($f['a']) ?></div></details>
<?php endforeach; ?>
  </section>
<?php endif; ?>

  <p class="sn-byline sn-byline-b"><?= h(T('by')) ?> <?= h(SITE_NAME) ?> | <?= h(T('updated')) ?> <time datetime="<?= h($u['updated']) ?>"><?= h(date(T('date_fmt'), strtotime($u['updated']))) ?></time></p>
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
    <li><a href="<?= url($gbase) ?>"><?= h(T('all_units')) ?> <?= h(gs($grade['name'], $subject['name'])) ?></a></li>
<?php foreach ($utopics as $tk => $tn): ?>
    <li><a href="<?= url($seg[0] . '/' . $seg[1] . '/topics/' . $tk . '/') ?>"><?= h($tn) ?></a></li>
<?php endforeach; ?>
  </ul>
  <h3><?= h(gs($grade['name'], $subject['name'])) ?></h3>
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
if (preg_match('/^grade-(\d+)$/', $grade['slug'], $gm) && ($country['code'] === 'us' || $country['code'] === 'us-tx' || $country['code'] === 'ph' || $country['code'] === 'za' || $country['code'] === 'tw' || $country['code'] === 'cn' || $country['code'] === 'kr' || strpos($country['code'], 'ca') === 0)) {   // Texas, the Philippines, Canada and Taiwan: Grade 3 = age 8-9, like the US
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);
} elseif ($grade['slug'] === 'okul-oncesi' && $country['code'] === 'tr') {
    $lr['typicalAgeRange'] = '5-6';   // Türkiye: okul öncesi 60-72 ay
    $lr['educationalLevel'] = array($grade['name'], 'Okul Öncesi Eğitim (60-72 ay)');
} elseif (preg_match('/^(\d+)-sinif$/', $grade['slug'], $gm) && $country['code'] === 'tr') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Türkiye: 3. sınıf = age 8-9
    $lr['educationalLevel'] = array($grade['name'], (int)$gm[1] <= 4 ? 'İlkokul' : ((int)$gm[1] <= 8 ? 'Ortaokul' : 'Lise'));
} elseif (preg_match('/^arskurs-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'se') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 6) . '-' . ((int)$gm[1] + 7);   // Sverige: årskurs 3 = age 9-10 (förskoleklass at 6)
    $lr['educationalLevel'] = array($grade['name'], (int)$gm[1] <= 3 ? 'Grundskolan, lågstadiet' : ((int)$gm[1] <= 6 ? 'Grundskolan, mellanstadiet' : 'Grundskolan, högstadiet'));
} elseif ($country['code'] === 'se' && $grade['slug'] === 'forskoleklass') {
    $lr['typicalAgeRange'] = '6-7';   // Sverige: förskoleklass, the year children turn 6
    $lr['educationalLevel'] = array($grade['name'], 'Förskoleklass');
} elseif ($country['code'] === 'se' && isset(array('matematik-1c' => 1, 'matematik-2c' => 1, 'matematik-3c' => 1, 'matematik-4' => 1, 'matematik-5' => 1)[$grade['slug']])) {
    $ages = array('matematik-1c' => '16-17', 'matematik-2c' => '16-18', 'matematik-3c' => '17-18', 'matematik-4' => '17-19', 'matematik-5' => '18-19');
    $lr['typicalAgeRange'] = $ages[$grade['slug']];   // Sverige, gymnasieskolan: nivå 1c–2c in year 1, 3c–4 in year 2, 5 in year 3
    $lr['educationalLevel'] = array($grade['name'], 'Gymnasieskolan');
} elseif (preg_match('/^kelas-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'id') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Indonesia: SD kelas 4 = age 9-10
    $lr['educationalLevel'] = array($grade['name'], (int)$gm[1] <= 6 ? 'Sekolah Dasar' : ((int)$gm[1] <= 9 ? 'Sekolah Menengah Pertama' : 'Sekolah Menengah Atas'));
} elseif ($country['code'] === 'cn' && isset(array('required-1' => 1, 'required-2' => 1, 'elective-1' => 1, 'elective-2' => 1, 'elective-3' => 1)[$grade['slug']])) {
    $ages = array('required-1' => '15-16', 'required-2' => '15-16', 'elective-1' => '16-17', 'elective-2' => '16-17', 'elective-3' => '16-18');
    $lr['typicalAgeRange'] = $ages[$grade['slug']];   // China, 普通高中: 必修 = 高一, 选择性必修 = 高二〜高三
    $lr['educationalLevel'] = array($grade['name'], '普通高中');
} elseif ($country['code'] === 'kr' && isset(array('common-math-1' => 1, 'common-math-2' => 1, 'algebra' => 1, 'calculus-1' => 1, 'probability-and-statistics' => 1)[$grade['slug']])) {
    $ages = array('common-math-1' => '15-16', 'common-math-2' => '15-16', 'algebra' => '16-17', 'calculus-1' => '16-17', 'probability-and-statistics' => '17-18');
    $lr['typicalAgeRange'] = $ages[$grade['slug']];   // Korea, 고등학교: 공통수학1·2 = 1학년, 대수·미적분Ⅰ = 2학년, 확률과 통계 = 2~3학년
    $lr['educationalLevel'] = array($grade['name'], '고등학교');
} elseif (preg_match('/^class-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'in') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // India: Class 10 = age 15-16
} elseif (preg_match('/^klasse-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'ch') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Schweiz (Lehrplan 21): 3. Klasse = age 8-9
    $lr['educationalLevel'] = array($grade['name'], (int)$gm[1] <= 6 ? 'Primarstufe' : 'Sekundarstufe I');
} elseif (preg_match('/^klasse-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'de') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Germany: Klasse 3 = age 8-9
} elseif ($country['code'] === 'fr' && isset(array('cp' => 1, 'ce1' => 1, 'ce2' => 1, 'cm1' => 1, 'cm2' => 1, '6e' => 1, '5e' => 1, '4e' => 1, '3e' => 1, 'seconde' => 1, 'premiere' => 1)[$grade['slug']])) {
    $fy = array('cp' => 6, 'ce1' => 7, 'ce2' => 8, 'cm1' => 9, 'cm2' => 10, '6e' => 11, '5e' => 12, '4e' => 13, '3e' => 14, 'seconde' => 15, 'premiere' => 16);   // France: CE2 = age 8-9
    $lr['typicalAgeRange'] = $fy[$grade['slug']] . '-' . ($fy[$grade['slug']] + 1);
} elseif ($country['code'] === 'it' && isset(array('classe-prima' => 1, 'classe-seconda' => 1, 'classe-terza' => 1, 'classe-quarta' => 1, 'classe-quinta' => 1, 'prima-media' => 1, 'seconda-media' => 1, 'terza-media' => 1, 'prima-liceo' => 1, 'seconda-liceo' => 1, 'terza-liceo' => 1, 'quarta-liceo' => 1, 'quinta-liceo' => 1)[$grade['slug']])) {
    $iy = array('classe-prima' => 6, 'classe-seconda' => 7, 'classe-terza' => 8, 'classe-quarta' => 9, 'classe-quinta' => 10, 'prima-media' => 11, 'seconda-media' => 12, 'terza-media' => 13, 'prima-liceo' => 14, 'seconda-liceo' => 15, 'terza-liceo' => 16, 'quarta-liceo' => 17, 'quinta-liceo' => 18);   // Italy: classe terza = age 8-9
    $lr['typicalAgeRange'] = $iy[$grade['slug']] . '-' . ($iy[$grade['slug']] + 1);
} elseif (preg_match('/^(\d)-ano$/', $grade['slug'], $gm) && $country['code'] === 'br') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Brazil: 1º ano = age 6-7, 3º ano = age 8-9
} elseif (preg_match('/^(\d)-primaria$/', $grade['slug'], $gm) && $country['code'] === 'es') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Spain: 4.º de Primaria = age 9-10
    $lr['educationalLevel'] = array($grade['name'], 'Educación Primaria');
} elseif ($grade['slug'] === 'preescolar' && $country['code'] === 'mx') {
    $lr['typicalAgeRange'] = '5-6';   // México: 3.er grado de preescolar (Fase 2)
    $lr['educationalLevel'] = array('3.er grado de preescolar', 'Educación preescolar');
} elseif (preg_match('/^(\d)-primaria$/', $grade['slug'], $gm) && $country['code'] === 'mx') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // México: 3.er grado de primaria = age 8-9
    $lr['educationalLevel'] = array($grade['name'], 'Educación primaria');
} elseif (preg_match('/^(\d)-secundaria$/', $grade['slug'], $gm) && $country['code'] === 'mx') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 11) . '-' . ((int)$gm[1] + 12);   // México: 1.er grado de secundaria = age 12-13
    $lr['educationalLevel'] = array($grade['name'], 'Educación secundaria');
} elseif ($country['code'] === 'mx' && isset(array('pensamiento-matematico-1' => 1, 'pensamiento-matematico-2' => 1, 'pensamiento-matematico-3' => 1, 'temas-selectos-1' => 1, 'temas-selectos-2' => 1)[$grade['slug']])) {
    $ages = array('pensamiento-matematico-1' => '15-16', 'pensamiento-matematico-2' => '15-16', 'pensamiento-matematico-3' => '16-17', 'temas-selectos-1' => '16-17', 'temas-selectos-2' => '17-18');
    $lr['typicalAgeRange'] = $ages[$grade['slug']];   // México, bachillerato (MCCEMS): Pensamiento Matemático I = 1.er semestre
    $lr['educationalLevel'] = array($grade['name'], 'Educación media superior (bachillerato)');
} elseif (preg_match('/^(\d)-eso$/', $grade['slug'], $gm) && $country['code'] === 'es') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 11) . '-' . ((int)$gm[1] + 12);   // Spain: 1.º de ESO = age 12-13
    $lr['educationalLevel'] = array($grade['name'], 'Educación Secundaria Obligatoria');
} elseif (preg_match('/^(\d)-bachillerato$/', $grade['slug'], $gm) && $country['code'] === 'es') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 15) . '-' . ((int)$gm[1] + 16);   // Spain: 1.º de Bachillerato = age 16-17
    $lr['educationalLevel'] = array($grade['name'], 'Bachillerato');
} elseif (preg_match('/^(\d)-bachillerato-ccss$/', $grade['slug'], $gm) && $country['code'] === 'es') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 15) . '-' . ((int)$gm[1] + 16);   // Spain: Matemáticas Aplicadas a las Ciencias Sociales I = age 16-17
    $lr['educationalLevel'] = array($grade['name'], 'Bachillerato');
} elseif (preg_match('/^(\d)-serie$/', $grade['slug'], $gm) && $country['code'] === 'br') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 14) . '-' . ((int)$gm[1] + 15);   // Brazil, Ensino Médio: 1ª série = age 15-16
    $lr['educationalLevel'] = array($grade['name'], 'Ensino Médio');
} elseif ($grade['slug'] === 'grade-r' && $country['code'] === 'za') {
    $lr['typicalAgeRange'] = '5-6';   // South Africa: Grade R (Reception Year), the year before Grade 1
    $lr['educationalLevel'] = array('Grade R', 'Reception Year');
} elseif ($grade['slug'] === 'kindergarten' && $country['code'] === 'kr') {
    $lr['typicalAgeRange'] = '5-6';   // Korea: 유치원 만 5세반 (2019 개정 누리과정)
    $lr['educationalLevel'] = array('유치원', '만 5세', '누리과정');
} elseif ($grade['slug'] === 'kindergarten' && $country['code'] === 'cn') {
    $lr['typicalAgeRange'] = '5-6';   // China: 幼儿园大班 (《3-6岁儿童学习与发展指南》)
    $lr['educationalLevel'] = array('幼儿园大班', '学前教育');
} elseif ($grade['slug'] === 'tk' && $country['code'] === 'id') {
    $lr['typicalAgeRange'] = '5-6';   // Indonesia: TK B (Taman Kanak-kanak), Fase Fondasi
    $lr['educationalLevel'] = array('TK B', 'Taman Kanak-kanak', 'PAUD');
} elseif (preg_match('/^gymnasium-(\d)$/', $grade['slug'], $gm) && $country['code'] === 'ch') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 14) . '-' . ((int)$gm[1] + 15);   // Switzerland: Gymnasium (4 years to the Matura), 1. Klasse = age 15-16
    $lr['educationalLevel'] = array('Gymnasium', 'Sekundarstufe II', 'Maturitätsschule');
} elseif ($grade['slug'] === 'kindergarten' && $country['code'] === 'ch') {
    $lr['typicalAgeRange'] = '4-6';   // Switzerland: 2 years of Kindergarten, Zyklus 1 of Lehrplan 21
    $lr['educationalLevel'] = array('Kindergarten', 'Zyklus 1');
} elseif ($grade['slug'] === 'kindergarten') {
    $lr['typicalAgeRange'] = '5-6';
} elseif ($grade['slug'] === 'algebra-1') {
    $lr['typicalAgeRange'] = '14-15';   // usually taken in Grade 9
} elseif ($grade['slug'] === 'geometry') {
    $lr['typicalAgeRange'] = '15-16';   // usually taken in Grade 10
} elseif ($grade['slug'] === 'algebra-2') {
    $lr['typicalAgeRange'] = '16-17';   // usually taken in Grade 11
} elseif ($grade['slug'] === 'precalculus') {
    $lr['typicalAgeRange'] = '17-18';   // usually taken in Grade 12
} elseif ($grade['slug'] === 'foundation') {
    $lr['typicalAgeRange'] = '5-6';   // Australia: first year of school
    // the same year has a different name in each state
    $lr['educationalLevel'] = array('Foundation', 'Prep', 'Kindergarten', 'Pre-primary', 'Reception', 'Transition');
} elseif (preg_match('/^year-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'uk') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 4) . '-' . ((int)$gm[1] + 5);   // England: Year 4 = age 8-9
} elseif (preg_match('/^year-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'au') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Australia: Year 3 = age 8-9
} elseif (preg_match('/^primary-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'ng') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Nigeria: Primary 1 at 6, Primary 4 = age 9-10
    $lr['educationalLevel'] = array($grade['name'], 'Primary school (9-Year Basic Education)');
} elseif (preg_match('/^jss-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'ng') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 11) . '-' . ((int)$gm[1] + 12);   // Nigeria: JSS 1 = age 12-13
    $lr['educationalLevel'] = array($grade['name'], 'Junior Secondary School (Upper Basic Education)');
} elseif (preg_match('/^primary-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'sg') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 5) . '-' . ((int)$gm[1] + 6);   // Singapore: Primary 4 = age 9-10
} elseif (preg_match('/^secondary-(\d+)$/', $grade['slug'], $gm) && $country['code'] === 'sg') {
    $lr['typicalAgeRange'] = ((int)$gm[1] + 11) . '-' . ((int)$gm[1] + 12);   // Singapore: Secondary 1 = age 12-13
}
if ($u['standard_code']) {
    $al = array('@type' => 'AlignmentObject', 'alignmentType' => 'teaches',
                'educationalFramework' => $std_name, 'targetName' => $u['standard_code'],
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
