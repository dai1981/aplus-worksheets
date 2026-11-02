<?php
/* Preview images (1200 x 630 PNG) for search results, social cards and Pinterest.
   /worksheets/{c}/{s}/{g}/{unit}/preview.png   one skill
   /worksheets/{c}/{s}/{g}/preview.png          one grade
   /worksheets/{c}/{s}/topics/{t}/preview.png   one topic
   Drawn with GD on each request (no files are written to the server) and cached by browsers and CDNs. */

function preview_supported() {
    return function_exists('imagecreatetruecolor') && function_exists('imagettftext');
}

/* question / choice HTML -> one line of plain text */
function pv_text($html) {
    $s = preg_replace("/<div class='qfig'>.*?<\\/div>/s", ' ', (string)$html);
    $s = preg_replace('/<svg.*?<\/svg>/s', ' ', $s);
    $s = preg_replace("/<span class='fn'>(.*?)<\\/span><span class='fd'>(.*?)<\\/span>/s", '$1/$2', $s);
    $s = preg_replace_callback('/<sup>(.*?)<\/sup>/s', function ($m) {      // 2<sup>3</sup> -> 2³
        $t = strip_tags($m[1]);
        $map = array('0' => '⁰', '1' => '¹', '2' => '²', '3' => '³', '4' => '⁴', '5' => '⁵', '6' => '⁶',
                     '7' => '⁷', '8' => '⁸', '9' => '⁹', '−' => '⁻', '-' => '⁻', '+' => '⁺', 'n' => 'ⁿ');
        $o = '';
        foreach (preg_split('//u', $t, -1, PREG_SPLIT_NO_EMPTY) as $ch) {
            if (!isset($map[$ch])) return '^' . $t;
            $o .= $map[$ch];
        }
        return $o;
    }, $s);
    $s = preg_replace('/<br\s*\/?>/i', ' ', $s);
    $s = html_entity_decode(strip_tags($s), ENT_QUOTES | ENT_HTML5, 'UTF-8');
    return trim(preg_replace('/[ \t\r\n]+/u', ' ', $s));
}

function pv_font($w) {
    $d = __DIR__ . '/../assets/fonts/';
    return $d . ($w === 'b' ? 'Inter-Bold.otf' : ($w === 'm' ? 'DejaVuSans.ttf' : 'Inter-Regular.otf'));
}
/* Inter has no glyph for a few maths signs: use DejaVu for those lines */
function pv_face($s, $w) {
    return preg_match('/[∛∠∡⊥∥]/u', $s) ? pv_font('m') : pv_font($w);
}
function pv_width($size, $font, $s) {
    $b = imagettfbbox($size, 0, $font, $s);
    return $b[2] - $b[0];
}
/* wrap text into lines no wider than $max; the last allowed line ends with … if cut */
function pv_wrap($s, $size, $font, $max, $lines) {
    $words = preg_split('/ /u', $s);
    $out = array(); $cur = '';
    foreach ($words as $w) {
        $try = $cur === '' ? $w : $cur . ' ' . $w;
        if (pv_width($size, $font, $try) <= $max || $cur === '') { $cur = $try; continue; }
        $out[] = $cur; $cur = $w;
        if (count($out) === $lines) break;
    }
    if (count($out) < $lines && $cur !== '') { $out[] = $cur; $cur = ''; }
    if ($cur !== '' || count($out) > $lines) {                        // text was cut
        $out = array_slice($out, 0, $lines);
        $last = $out[$lines - 1];
        while ($last !== '' && pv_width($size, $font, $last . '…') > $max) {
            $last = preg_replace('/\s*\S+$/u', '', $last);
        }
        $out[$lines - 1] = rtrim($last, ' ,;:') . '…';
    }
    return $out;
}
function pv_color($im, $hex) {
    return imagecolorallocate($im, hexdec(substr($hex, 1, 2)), hexdec(substr($hex, 3, 2)), hexdec(substr($hex, 5, 2)));
}
function pv_rrect($im, $x1, $y1, $x2, $y2, $r, $col) {
    imagefilledrectangle($im, $x1 + $r, $y1, $x2 - $r, $y2, $col);
    imagefilledrectangle($im, $x1, $y1 + $r, $x2, $y2 - $r, $col);
    foreach (array(array($x1 + $r, $y1 + $r), array($x2 - $r, $y1 + $r), array($x1 + $r, $y2 - $r), array($x2 - $r, $y2 - $r)) as $c) {
        imagefilledellipse($im, $c[0], $c[1], 2 * $r, 2 * $r, $col);
    }
}
function pv_logo($im, $cx, $cy, $r, $col) {     // the Aplus hexagon cube
    imagesetthickness($im, max(2, (int)round($r / 5)));
    $p = array();
    for ($i = 0; $i < 6; $i++) {
        $a = deg2rad(-90 + 60 * $i);
        $p[] = array($cx + $r * cos($a), $cy + $r * sin($a));
    }
    for ($i = 0; $i < 6; $i++) {
        $q = $p[($i + 1) % 6];
        imageline($im, (int)$p[$i][0], (int)$p[$i][1], (int)$q[0], (int)$q[1], $col);
    }
    imageline($im, (int)$p[5][0], (int)$p[5][1], $cx, $cy, $col);
    imageline($im, (int)$p[1][0], (int)$p[1][1], $cx, $cy, $col);
    imageline($im, $cx, $cy, $cx, (int)$p[3][1], $col);
    imagesetthickness($im, 1);
}

/* $c: label, title, chips[], paper_title, paper_sub, lines[] (each [text, sub]), mode quiz|list, foot */
function preview_render($c) {
    $W = 1200; $H = 630;
    $im = imagecreatetruecolor($W, $H);
    imagealphablending($im, true);
    $bg = pv_color($im, '#f7f3ea'); $green = pv_color($im, '#006633'); $ink = pv_color($im, '#1f2522');
    $muted = pv_color($im, '#6f675d'); $white = pv_color($im, '#ffffff'); $line = pv_color($im, '#e3dccf');
    $soft = pv_color($im, '#e6f0ea'); $red = pv_color($im, '#c0392b');
    imagefilledrectangle($im, 0, 0, $W, $H, $bg);
    imagefilledrectangle($im, 0, 0, $W, 14, $green);

    // ---- right: a worksheet page
    $px1 = 690; $py1 = 58; $px2 = 1150; $py2 = 650;
    $sh = imagecolorallocatealpha($im, 70, 55, 30, 122);   // soft shadow
    for ($i = 8; $i >= 1; $i--) pv_rrect($im, $px1 + $i, $py1 + 2 + $i, $px2 + $i, $py2 + $i, 12, $sh);
    pv_rrect($im, $px1, $py1, $px2, $py2, 10, $white);
    $x = $px1 + 30; $y = $py1 + 44;
    imagettftext($im, 13, 0, $x, $y, $muted, pv_font('r'), 'Name ______________   Date ________');
    $y += 40;
    foreach (pv_wrap($c['paper_title'], 22, pv_font('b'), $px2 - $px1 - 60, 2) as $l) {
        imagettftext($im, 22, 0, $x, $y, $ink, pv_face($l, 'b'), $l); $y += 32;
    }
    imagettftext($im, 13, 0, $x, $y, $green, pv_font('b'), strtoupper($c['paper_sub']));
    $y += 16;
    imagesetthickness($im, 2); imageline($im, $x, $y, $px2 - 30, $y, $line); imagesetthickness($im, 1);
    $y += 34;
    $n = 0;
    foreach ($c['lines'] as $ln) {
        if ($y > $py2 - 40) break;
        $n++;
        $txt = $ln[0];
        if ($c['mode'] === 'quiz') {
            imagettftext($im, 15, 0, $x, $y, $green, pv_font('b'), $n . '.');
            $rows = pv_wrap($txt, 15, pv_face($txt, 'r'), $px2 - $x - 60, 2);
            foreach ($rows as $r) { imagettftext($im, 15, 0, $x + 30, $y, $ink, pv_face($r, 'r'), $r); $y += 23; }
            if (!empty($ln[1])) {
                $ch = pv_wrap($ln[1], 13, pv_face($ln[1], 'r'), $px2 - $x - 60, 1);
                imagettftext($im, 13, 0, $x + 30, $y, $muted, pv_face($ch[0], 'r'), $ch[0]); $y += 22;
            }
            $y += 18;
        } else {
            imagerectangle($im, $x, $y - 15, $x + 16, $y + 1, $green);
            $rows = pv_wrap($txt, 16, pv_face($txt, 'b'), $px2 - $x - 70, 1);
            imagettftext($im, 16, 0, $x + 30, $y, $ink, pv_face($rows[0], 'b'), $rows[0]);
            if (!empty($ln[1])) {
                imagettftext($im, 12, 0, $x + 30, $y + 20, $muted, pv_font('r'), $ln[1]); $y += 20;
            }
            $y += 34;
        }
    }

    // ---- left: what this is
    $lx = 64;
    pv_logo($im, $lx + 18, 74, 18, $green);
    imagettftext($im, 22, 0, $lx + 48, 83, $green, pv_font('b'), SITE_NAME . ' Worksheets');
    $y = 150;
    foreach (pv_wrap(strtoupper($c['label']), 15, pv_font('b'), 580, 2) as $l) {
        imagettftext($im, 15, 0, $lx, $y, $muted, pv_face($l, 'b'), $l); $y += 24;
    }
    $y += 34;
    $size = 60; $tl = pv_wrap($c['title'], $size, pv_font('b'), 590, 3);
    while ($size > 40 && (count($tl) > 2 || substr(end($tl), -3) === '…')) {
        $size -= 4; $tl = pv_wrap($c['title'], $size, pv_font('b'), 590, 3);
    }
    foreach ($tl as $l) { imagettftext($im, $size, 0, $lx, $y + $size, $ink, pv_face($l, 'b'), $l); $y += (int)($size * 1.22); }
    $y += 36;
    $cx = $lx;
    foreach ($c['chips'] as $chip) {
        $w = pv_width(16, pv_font('b'), $chip) + 34;
        if ($cx + $w > 640) { $cx = $lx; $y += 54; }
        pv_rrect($im, $cx, $y, $cx + $w, $y + 40, 20, $soft);
        imagettftext($im, 16, 0, $cx + 17, $y + 27, $green, pv_font('b'), $chip);
        $cx += $w + 12;
    }
    imagettftext($im, 16, 0, $lx, $H - 48, $muted, pv_font('r'), $c['foot']);
    imagefilledrectangle($im, $lx, $H - 80, $lx + 56, $H - 76, $red);

    header('Content-Type: image/png');
    header('Cache-Control: public, max-age=604800');
    imagepng($im, null, 6);
    imagedestroy($im);
}

/* the ETag only changes when the data behind the picture changes */
function preview_cache_check($tag) {
    $etag = '"pv-' . md5($tag . '|v3') . '"';
    header('ETag: ' . $etag);
    if (isset($_SERVER['HTTP_IF_NONE_MATCH']) && trim($_SERVER['HTTP_IF_NONE_MATCH']) === $etag) {
        http_response_code(304);
        exit;
    }
}

function preview_route($seg) {
    if (!preview_supported()) { http_response_code(404); exit; }
    $country = get_country($seg[0]);
    $subject = $country ? get_subject($seg[0], $seg[1]) : null;
    if (!$subject) { http_response_code(404); exit; }
    T(array($country['lang']));
    $paper = strtoupper($country['paper']);
    $foot = 'Free · apu2.com/worksheets';

    if (count($seg) === 4 && $seg[2] === 'topics') {                  // topic
        require_once __DIR__ . '/topics.php';
        $all = topics_for($seg[0], $seg[1]);
        $defs = topic_defs();
        if (!isset($all[$seg[3]])) { http_response_code(404); exit; }
        $units = $all[$seg[3]];
        preview_cache_check(json_encode(array_map(function ($u) { return $u['slug'] . $u['updated']; }, $units)));
        $name = topic_name($defs[$seg[3]], $seg[0]);
        $lines = array();
        foreach ($units as $u) $lines[] = array($u['short_title'], $u['grade_name']);
        preview_render(array(
            'label' => topic_range($units) . ' · ' . $country['standard'],
            'title' => $name . ' Worksheets',
            'chips' => array(count($units) . ' skills', 'Lessons', 'Answer keys'),
            'paper_title' => $name, 'paper_sub' => $subject['name'] . ' · ' . $country['name'],
            'lines' => $lines, 'mode' => 'list', 'foot' => $foot));
        exit;
    }

    $grade = get_grade($seg[0], $seg[1], $seg[2]);
    if (!$grade) { http_response_code(404); exit; }

    if (count($seg) === 3) {                                           // grade
        $units = list_units($seg[0], $seg[1], $seg[2]);
        if (!$units) { http_response_code(404); exit; }
        preview_cache_check(json_encode($units));
        $lines = array();
        foreach ($units as $u) $lines[] = array($u['short_title'], '');
        preview_render(array(
            'label' => $country['standard'] . ' · ' . $country['name'],
            'title' => $grade['name'] . ' ' . $subject['name'] . ' Worksheets',
            'chips' => array(count($units) . ' skills', '100 questions each', 'Answer keys'),
            'paper_title' => $grade['name'] . ' ' . $subject['name'], 'paper_sub' => count($units) . ' skills',
            'lines' => $lines, 'mode' => 'list', 'foot' => $foot));
        exit;
    }

    $u = get_unit($seg[0], $seg[1], $seg[2], $seg[3]);                // one skill
    if (!$u) { http_response_code(404); exit; }
    preview_cache_check($u['updated'] . $u['title'] . $u['short_title']);
    $sets = json_decode($u['sets_json'], true);
    $lines = array();
    foreach (array_slice($sets, 1) as $set) {                          // practice sets, not the warm-up
        foreach ($set['items'] as $it) {
            $q = pv_text($it['q']);
            if ($q === '' || mb_strlen($q) > 120) continue;
            $ch = array();
            foreach ($it['c'] as $k => $cc) $ch[] = ($k + 1) . ') ' . pv_text($cc);
            $lines[] = array($q, implode('   ', $ch));
            if (count($lines) >= 6) break 2;
        }
    }
    preview_render(array(
        'label' => $grade['name'] . ' ' . $subject['name']
                   . ($u['standard_code'] ? ' · ' . preg_replace('/^' . preg_quote($grade['name'], '/') . ':\s*/', '', $u['standard_code']) : ''),
        'title' => $u['short_title'],
        'chips' => array('Lesson', '100 questions', 'Printable ' . ($paper === 'LETTER' ? 'Letter' : $paper), 'Answer key'),
        'paper_title' => $u['short_title'], 'paper_sub' => 'Practice · ' . $grade['name'],
        'lines' => $lines, 'mode' => 'quiz', 'foot' => $foot));
    exit;
}
