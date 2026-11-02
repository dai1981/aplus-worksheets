<?php
/* =========================================================
   Aplus worksheets  設定ファイル
   DB の接続情報は既存の /common/php/dbConnection.php を読み込んで使う
   （パスワードをここに書かない）
   ========================================================= */

// --- 既存の接続設定（$DB_HOST / $DB_USER / $DB_PASS / $DB_NAME / $DB_PORT）
$__dbconf = array(
    '/home/users/1/lolipop.jp-dp07302908/web/common/php/dbConnection.php', // サーバーの絶対パス
    __DIR__ . '/../../../common/php/dbConnection.php',                      // /aplus/worksheets/inc/ から見た位置
);
foreach ($__dbconf as $__f) {
    if (is_file($__f)) { require_once $__f; break; }
}
if (empty($DB_HOST)) { http_response_code(503); exit('DB settings not found.'); }

// ワークシートは自前の接続を使う（既存の持続接続の文字コードを変えないため）
define('DB_DSN', 'mysql:host=' . $DB_HOST . ';port=' . (isset($DB_PORT) ? $DB_PORT : '3306')
               . ';dbname=' . $DB_NAME . ';charset=utf8mb4');
define('DB_USER', $DB_USER);
define('DB_PASS', $DB_PASS);

// --- URL（apu2.com の公開フォルダ /aplus/ の中に worksheets/ を置く前提）
define('BASE_URL',  'https://www.apu2.com/worksheets');  // 末尾スラッシュなし
define('BASE_PATH', '/worksheets');                   // 末尾スラッシュなし

// --- サイト名・ブランド
define('SITE_NAME', 'Aplus');
define('SITE_HOME', 'https://www.apu2.com/');

// --- 計測・広告（空のままなら出力しない）
define('GA_ID', '');             // 例 G-XXXXXXXXXX
define('ADSENSE_CLIENT', '');    // 例 ca-pub-3234684892462480

// --- CSS/JS を更新したら数字を変える（ブラウザのキャッシュ対策）
define('ASSET_VER', '20261102c');

// --- ページのキャッシュ（秒）。0 で無効
define('PAGE_MAX_AGE', 3600);
