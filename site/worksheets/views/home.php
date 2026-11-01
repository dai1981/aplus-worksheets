<?php
$countries = qa('SELECT * FROM ws_country ORDER BY sort, name');
$subjects = qa('SELECT * FROM ws_subject ORDER BY sort, name');

page_head(array(
    'title' => 'Free Printable Worksheets by Country and Grade | ' . SITE_NAME,
    'desc' => 'Free printable worksheets and online practice that follow your country\'s curriculum. Short lessons, 100 practice questions per skill and answer keys.',
    'canonical' => '',
));
site_header(array());
?>
<main class="sn-wrap">
<h1>Free Worksheets for Your Curriculum</h1>
<div class="sx-hero"><p>Pick your country. Every skill comes with a short lesson, <b>100 practice questions</b> and a <b>printable worksheet with an answer key</b>.</p></div>
<?php foreach ($countries as $c): ?>
<h2><?= h($c['name']) ?></h2>
<p class="ws-lead"><?= h($c['intro']) ?></p>
<ul class="sx-grades">
<?php foreach ($subjects as $s): if ($s['country'] !== $c['code']) continue; ?>
  <li><a href="<?= url($c['code'] . '/' . $s['slug'] . '/') ?>"><?= h($s['name']) ?><span class="n"><?= h($c['standard']) ?></span></a></li>
<?php endforeach; ?>
</ul>
<?php endforeach; ?>
</main>
<?php
echo jsonld(array('@context' => 'https://schema.org', '@type' => 'WebSite',
                  'name' => SITE_NAME . ' Worksheets', 'url' => abs_url('')));
site_footer('en', false);
?>
</body>
</html>
