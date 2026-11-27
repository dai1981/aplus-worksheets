<?php
/* Quiz together API for apu2.com (/worksheets/api/mq.php)
   The real code is one shared file on the same server: eigo-duke.com /common/php/mq.php
   (DB: mysql150, tables qz_room / qz_player only).
   $MQ_EST_FILE: provisional accuracy per subject / grade / unit, shown as an "estimate" until an area has enough
   players (../inc/mq-est.json). It is never written to the DB; real numbers replace it automatically. */
$MQ_EST_FILE = __DIR__ . '/../inc/mq-est.json';
/* $MQ_FIELD_FILE: unit pages per field (fractions, ratios, …) to compare countries by field (../inc/mq-fields.json, tools/build_mq_fields.php). */
$MQ_FIELD_FILE = __DIR__ . '/../inc/mq-fields.json';
$__mq = array(
    '/home/users/1/lolipop.jp-dp07302908/web/common/php/mq.php',  // server path
    __DIR__ . '/../../../common/php/mq.php',                        // from /aplus/worksheets/api/
);
foreach ($__mq as $__f) {
    if (is_file($__f)) { require $__f; exit; }
}
http_response_code(503);
header('Content-Type: application/json; charset=utf-8');
echo '{"err":"setup"}';
