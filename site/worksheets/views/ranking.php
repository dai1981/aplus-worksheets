<?php
/* Quiz together rankings: class accuracy by country and by state / province (/worksheets/ranking/)
   The page is drawn by one shared file on eigo-duke.com: /common/js/mq-rank.js (data: api/mq.php?a=rank) */
page_head(array(
    'title' => 'Quiz Together Rankings: Class Accuracy by Country and State | ' . SITE_NAME,
    'desc' => 'See how classes in your state, province or country score on Quiz Together. Play a quiz together with your class and help your area climb the ranking.',
    'canonical' => 'ranking/',
));
site_header(array());
?>
<main class="sn-wrap">
<div id="mq-rank-app"></div>
<p class="mqr-intro">Quiz Together lets a class answer the same quiz on their phones. Tap the small QR code on any quiz, choose your country and area on the waiting screen, and your class's accuracy counts toward your area's ranking. Only each player's first game counts, and names are never saved. An area's accuracy appears after enough players join.</p>
</main>
<style>.mqr-intro{max-width:860px;margin:18px auto 30px;font-size:14px;line-height:1.9;color:#5b5249}</style>
<script>window.MQR_CONF = { api: "<?= url('api/mq.php') ?>", lang: "en", quiz: "<?= url('') ?>" };</script>
<script src="https://www.eigo-duke.com/common/js/mq-geo.js?v=20261124a"></script>
<script src="https://www.eigo-duke.com/common/js/mq-rank.js?v=20261124a"></script>
<?php site_footer('en', false); ?>
</body>
</html>
