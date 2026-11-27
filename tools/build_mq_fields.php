<?php
/* php tools/build_mq_fields.php
   Writes site/worksheets/inc/mq-fields.json: {"v": date, "f": {field: ["us/math/grade-3/fractions", …]}}
   for comparing countries by field in the Quiz Together ranking (inc/fields.php, eigo-duke.com /common/php/mq.php).
   Run after adding units (Actions also runs it before the FTP upload). */
$root = dirname(__DIR__);
chdir($root . '/site/worksheets');
require 'inc/core.php';
require 'inc/topics.php';
require 'inc/fields.php';
$out = array();
foreach (mq_fields() as $k => $v) $out[$k] = array();
$n = 0; $none = array();
foreach (glob($root . '/content/*/*/*/*.json') as $f) {
    $p = explode('/', substr($f, strlen($root) + 9, -5));      // country/subject/grade/slug
    if (count($p) !== 4) continue;
    list($c, $s, $g, $slug) = $p;
    if (!preg_match('/^mat|^science$/', $s)) continue;
    $fs = unit_fields($c, $s, $slug);
    if (!$fs) $none[] = "$c/$s/$g/$slug";
    foreach ($fs as $fd) { $out[$fd][] = "$c/$s/$g/$slug"; $n++; }
}
foreach ($out as $k => $v) sort($out[$k]);
$json = json_encode(array('f' => $out), JSON_UNESCAPED_SLASHES);
$dst = $root . '/site/worksheets/inc/mq-fields.json';
if (!is_file($dst) || file_get_contents($dst) !== $json) file_put_contents($dst, $json);
fwrite(STDERR, "mq-fields.json: $n entries, " . strlen($json) . " bytes\n");
foreach ($out as $k => $v) fwrite(STDERR, sprintf("  %-18s %d\n", $k, count($v)));
fwrite(STDERR, count($none) . " unit(s) in no field" . ($none ? ": " . implode(" ", array_slice($none, 0, 60)) : "") . "\n");
