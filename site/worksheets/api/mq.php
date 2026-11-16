<?php
/* Quiz together API for apu2.com (/worksheets/api/mq.php)
   The real code is one shared file on the same server: eigo-duke.com /common/php/mq.php
   (DB: mysql150, tables qz_room / qz_player only). */
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
