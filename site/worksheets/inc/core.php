<?php
/* Aplus worksheets: shared helpers (DB, URLs, text, layout) */

require __DIR__ . '/config.php';

/* ---------------------------------------------------------------- DB */
function db() {
    static $pdo = null;
    if ($pdo === null) {
        $pdo = new PDO(DB_DSN, DB_USER, DB_PASS, array(
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ));
    }
    return $pdo;
}
function q1($sql, $args = array()) {
    $st = db()->prepare($sql);
    $st->execute($args);
    $r = $st->fetch();
    return $r ? $r : null;
}
function qa($sql, $args = array()) {
    $st = db()->prepare($sql);
    $st->execute($args);
    return $st->fetchAll();
}

/* ---------------------------------------------------------------- text */
function h($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
function url($path = '') {           // url('us/math/') -> /worksheets/us/math/
    return BASE_PATH . '/' . ltrim($path, '/');
}
function abs_url($path = '') { return BASE_URL . '/' . ltrim($path, '/'); }
function jsonld($data) {
    return '<script type="application/ld+json">'
        . json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG)
        . "</script>\n";
}
function strip_figs($html) {         // text of a question without its picture
    return trim(preg_replace("/<div class='qfig'>.*?<\\/div>/s", '', $html));
}
function has_fig($html) { return strpos($html, "<div class='qfig'>") !== false; }

/* UI text. Add a language by adding a block (key = ws_country.lang). */
function T($key = null) {
    static $T = array(
        'en' => array(
            'home' => 'Worksheets', 'grades' => 'Grades', 'units' => 'skills',
            'questions' => 'questions', 'points' => 'Key idea', 'quiz100' => '100-Question Practice',
            'quiz_lead' => '5 sets of 20 questions. You get the answer and a hint right away.',
            'learn_quiz' => 'Lesson + 100 questions', 'print' => 'Printable', 'pdf' => 'PDF',
            'your_score' => 'Your score', 'clear_grade' => 'Clear scores for this grade',
            'hook_title' => '100-question practice', 'hook_sub' => '5 sets of 20 · instant feedback',
            'hook_go' => 'Start practicing', 'faq' => 'Frequently asked questions',
            'related' => 'Keep learning', 'prev' => 'Previous', 'next_u' => 'Next',
            'all_units' => 'All skills in', 'printable_of' => 'Printable worksheet with answer key',
            'standard' => 'Standard', 'updated' => 'Updated', 'by' => 'By',
            'pick_grade' => 'Choose a grade', 'pick_subject' => 'Choose a subject',
            'print_sheets' => 'Printable worksheets',
            'print_note' => '4 pages: Warm-up, Practice 1, Practice 2, Answer key',
            'print_btn' => 'Print / Save as PDF', 'pdf_btn' => 'Download PDF',
            'lesson_link' => 'Lesson and online practice',
            'p_warmup' => 'Warm-up', 'p_prac1' => 'Practice 1', 'p_prac2' => 'Practice 2',
            'p_key' => 'Answer key', 'name' => 'Name', 'date' => 'Date', 'score' => 'Score',
            'circle' => 'Circle the number of the correct answer.', 'total_q' => '%d questions',
            'for_check' => 'For checking',
            'license' => 'Free to print and copy for home and classroom use.',
            'worksheets' => 'Worksheets', 'grade_ws' => '%s %s Worksheets',
            'notfound' => 'Page not found', 'back_home' => 'Back to all worksheets',
            'skills_count' => '%d skills', 'free' => 'Free · no sign-up',
            'by_grade' => 'by Grade',
        ),
    );
    // British English (UK pages): same as 'en' except these words
    if (!isset($T['en-GB'])) {
        $T['en-GB'] = array_merge($T['en'], array(
            'grades' => 'Years', 'pick_grade' => 'Choose a year', 'clear_grade' => 'Clear scores for this year',
            'hook_go' => 'Start practising', 'by_grade' => 'by Year',
        ));
    }
    if (!isset($T['en-AU'])) $T['en-AU'] = $T['en-GB'];   // Australian English: same words as British
    static $lang = 'en';
    if (is_array($key)) { $lang = isset($T[$key[0]]) ? $key[0] : 'en'; return null; } // set language
    if ($key === null) return $T[$lang];
    return isset($T[$lang][$key]) ? $T[$lang][$key] : $key;
}

/* text used by ws.js (quiz, scores, effects) */
function js_text($lang) {
    $J = array(
        'en' => array(
            'ok' => 'Correct!', 'ng' => 'Not quite', 'ans' => 'Answer:', 'next' => 'Next',
            'result' => 'See results', 'done' => 'Done', 'practice' => 'Practice',
            'score' => '<b>{o}</b> of {n} correct', 'best' => 'Your best: {o} / {t}',
            'm100' => 'All correct! You are ready for the next set.',
            'm80' => 'Almost there. Redo just the ones you missed.',
            'mlow' => 'Read the examples above, then try this set again.',
            'redoMiss' => 'Redo the {n} you missed', 'redoAll' => 'Start over',
            'loadErr' => 'Could not load the questions.', 'notYet' => 'Not yet',
            'total' => '<b>{o}</b> / {t} correct', 'mastered' => '({c} / {u} skills mastered)',
            'confirm' => 'Clear all saved scores for this grade?',
            'hook0' => 'Not started yet. Begin with set 1 (20 questions).',
            'hookAll' => 'All 5 sets mastered! Come back anytime to review.',
            'hookSome' => 'Mastered {d} of {n} sets. {r} more to go!',
            'okWords' => array('Correct!', 'Nice!', 'Great job!', 'You got it!', 'Well done!'),
            'ngWords' => array('Almost!', 'Try the next one!', 'Keep going!'),
            'streak' => array('3' => '3 in a row!', '5' => '5 in a row!', '10' => '10 in a row!',
                              '15' => '15 in a row!', '20' => 'Perfect set!'),
            'perfect' => 'Perfect score!', 'good' => 'Great work!',
            // ranks
            'tier' => array('above' => 'Above Average', 'sight' => 'Top in Sight', 'class' => 'Top of the Class',
                            'grade' => 'Top of the Grade', 'state' => 'Top in the State',
                            'nation' => 'Top in the Nation', 'world' => 'Top in the World'),
            'start' => 'Start', 'yourRank' => 'Your {name} rank', 'rankOf' => '{name} rank',
            'correct' => 'correct answers', 'todayPlus' => 'today +{n}',
            'more' => '<b>{n}</b> more correct answers to reach {t}',
            'toGo' => '{n} more to {t}', 'reachedBtn' => 'Reached! See your next goal',
            'allDone' => 'You reached every rank!', 'lap' => '{n} lap', 'laps' => '{n} laps',
            'ranks' => 'Ranks', 'locked' => '{n} more ranks above', 'lockedHint' => 'Unlocks as you climb', 'reached' => 'Reached', 'toGoShort' => '{n} to go', 'you' => 'You',
            'how' => '1 lap = every {name} question answered correctly once ({n} answers). Each skill counts up to the lap you are on, so keep every skill going.',
            'levelUp' => 'Level up!', 'keepGoing' => 'Keep going to {t}', 'yay' => 'Awesome',
            'achieved' => 'Goal reached!', 'ask' => 'Go for <b>{t}</b> next ({l})?',
            'goFor' => 'Go for it', 'later' => 'Later', 'notStarted' => 'Not started',
        ),
    );
    $J['en-GB'] = array_merge($J['en'], array(
        'confirm' => 'Clear all saved scores for this year?',
        'tier' => array('above' => 'Above Average', 'sight' => 'Top in Sight', 'class' => 'Top of the Class',
                        'grade' => 'Top of the Year', 'state' => 'Top in the County',
                        'nation' => 'Top in the Country', 'world' => 'Top in the World'),
    ));
    $J['en-AU'] = array_merge($J['en'], array(
        'confirm' => 'Clear all saved scores for this year?',
        'tier' => array('above' => 'Above Average', 'sight' => 'Top in Sight', 'class' => 'Top of the Class',
                        'grade' => 'Top of the Year', 'state' => 'Top in the State',
                        'nation' => 'Top in the Country', 'world' => 'Top in the World'),
    ));
    return isset($J[$lang]) ? $J[$lang] : $J['en'];
}

/* ---------------------------------------------------------------- layout */
function page_head($o) {
    // $o: lang, title, desc, canonical(path), og_type, hreflang, body_class, noindex
    $lang = isset($o['lang']) ? $o['lang'] : 'en';
    $can = abs_url($o['canonical']);
    if (PAGE_MAX_AGE > 0) header('Cache-Control: public, max-age=' . PAGE_MAX_AGE);
    header('Content-Type: text/html; charset=UTF-8');
    echo "<!DOCTYPE html>\n<html lang=\"" . h($lang) . "\">\n<head>\n<meta charset=\"UTF-8\">\n";
    echo "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n";
    echo '<title>' . h($o['title']) . "</title>\n";
    echo '<meta name="description" content="' . h($o['desc']) . "\">\n";
    echo '<meta name="robots" content="' . (empty($o['noindex']) ? 'index,follow,max-image-preview:large' : 'noindex,follow') . "\">\n";
    echo '<link rel="canonical" href="' . h($can) . "\">\n";
    if (!empty($o['hreflang'])) {
        echo '<link rel="alternate" hreflang="' . h($o['hreflang']) . '" href="' . h($can) . "\">\n";
    }
    echo '<meta property="og:type" content="' . h(isset($o['og_type']) ? $o['og_type'] : 'website') . "\">\n";
    echo '<meta property="og:site_name" content="' . h(SITE_NAME) . "\">\n";
    echo '<meta property="og:title" content="' . h($o['title']) . "\">\n";
    echo '<meta property="og:description" content="' . h($o['desc']) . "\">\n";
    echo '<meta property="og:url" content="' . h($can) . "\">\n";
    echo "<meta name=\"twitter:card\" content=\"summary\">\n";
    $css = isset($o['css']) ? $o['css'] : 'ws.css';
    echo '<link rel="icon" type="image/svg+xml" href="' . url('assets/logo.svg') . "\">\n";
    echo '<link rel="stylesheet" href="' . url('assets/' . $css) . '?v=' . ASSET_VER . "\">\n";
    if (!empty($o['head'])) echo $o['head'];
    if (GA_ID) {
        echo '<script async src="https://www.googletagmanager.com/gtag/js?id=' . h(GA_ID) . "\"></script>\n";
        echo "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','" . h(GA_ID) . "');</script>\n";
    }
    if (ADSENSE_CLIENT) {
        echo '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' . h(ADSENSE_CLIENT) . "\" crossorigin=\"anonymous\"></script>\n";
    }
    echo "</head>\n<body class=\"" . h(isset($o['body_class']) ? $o['body_class'] : 'ws-page') . "\">\n";
}

function site_header($crumbs) {
    // $crumbs: array of [label, path] ; the last one is the current page
    echo '<header class="ws-top"><div class="ws-top-in">';
    echo '<a class="ws-brand" href="' . h(SITE_HOME) . '">' . brand_svg() . '<span>' . h(SITE_NAME) . '</span></a>';
    echo '<a class="ws-top-link" href="' . url('') . '">' . h(T('worksheets')) . '</a>';
    echo "</div></header>\n";
    if ($crumbs) {
        echo '<nav class="ws-crumb" aria-label="Breadcrumb"><ol>';
        $n = count($crumbs);
        foreach ($crumbs as $i => $c) {
            if ($i === $n - 1) echo '<li aria-current="page">' . h($c[0]) . '</li>';
            else echo '<li><a href="' . url($c[1]) . '">' . h($c[0]) . '</a></li>';
        }
        echo "</ol></nav>\n";
    }
}

function breadcrumb_ld($crumbs) {
    $items = array();
    foreach ($crumbs as $i => $c) {
        $items[] = array('@type' => 'ListItem', 'position' => $i + 1,
                         'name' => $c[0], 'item' => abs_url($c[1]));
    }
    return jsonld(array('@context' => 'https://schema.org', '@type' => 'BreadcrumbList',
                        'itemListElement' => $items));
}

function site_footer($lang = 'en', $with_js = true) {
    echo '<footer class="ws-foot"><div class="ws-foot-in">';
    echo '<p><a href="' . url('') . '">' . h(T('worksheets')) . '</a> · <a href="' . h(SITE_HOME) . '">' . h(SITE_NAME) . '</a></p>';
    echo '<p class="c">&copy; ' . date('Y') . ' ' . h(SITE_NAME) . '. ' . h(T('license')) . '</p>';
    echo "</div></footer>\n";
    if ($with_js) {
        echo '<script>window.WS_T=' . json_encode(js_text($lang), JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . ";</script>\n";
        echo '<script src="' . url('assets/ws.js') . '?v=' . ASSET_VER . "\" defer></script>\n";
    }
}

function brand_svg() {
    return '<svg class="ws-logo" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">'
         . '<path d="M12 2.5 20.2 7.2v9.6L12 21.5 3.8 16.8V7.2Z M3.8 7.2 12 11.9 20.2 7.2 M12 11.9v9.6" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/></svg>';
}
function arrow_svg() {
    return '<svg class="ar" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>';
}

function not_found() {
    http_response_code(404);
    page_head(array('title' => T('notfound') . ' | ' . SITE_NAME, 'desc' => T('notfound'),
                    'canonical' => '', 'noindex' => true));
    site_header(array());
    echo '<main class="sn-wrap"><h1>' . h(T('notfound')) . '</h1><p><a href="' . url('') . '">'
       . h(T('back_home')) . "</a></p></main>\n";
    site_footer('en', false);
    echo "</body>\n</html>";
    exit;
}

/* ---------------------------------------------------------------- data */
function get_country($c) { return q1('SELECT * FROM ws_country WHERE code=?', array($c)); }
function get_subject($c, $s) { return q1('SELECT * FROM ws_subject WHERE country=? AND slug=?', array($c, $s)); }
function get_grade($c, $s, $g) { return q1('SELECT * FROM ws_grade WHERE country=? AND subject=? AND slug=?', array($c, $s, $g)); }
function get_unit($c, $s, $g, $u) {
    return q1('SELECT * FROM ws_unit WHERE country=? AND subject=? AND grade=? AND slug=?', array($c, $s, $g, $u));
}
function list_units($c, $s, $g, $full = false) {
    $cols = $full ? '*' : 'slug,title,short_title,domain,standard_code,pdf_url,sort,updated';
    return qa("SELECT $cols FROM ws_unit WHERE country=? AND subject=? AND grade=? ORDER BY sort, slug",
              array($c, $s, $g));
}
/* rank block: <div data-lv=...>. mode = card | mini | tile */
function rank_attrs($c, $s, $g, $units, $name, $mode) {
    $list = array();
    foreach ($units as $u) $list[] = array(prog_key($c, $s, $g, $u['slug']), 5);
    return ' data-lv="' . h(prog_key($c, $s, $g)) . '" data-lv-mode="' . h($mode) . '" data-lv-name="' . h($name)
         . '" data-lv-units="' . h(json_encode($list)) . '"';
}
function prog_key($c, $s, $g, $u = '') {   // localStorage key prefix
    return $c . '-' . $s . '-' . $g . ($u !== '' ? '-' . $u : '');
}
