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
            'by_grade' => 'by Grade', 'pin_save' => 'Save to Pinterest',
            // sentences built with sprintf (each language puts the words in its own order)
            'grade_title_sfx' => ': Free Printable + Online Practice',
            'grade_desc' => 'Free %1$s %2$s worksheets aligned to the %3$s: %4$s. 100 practice questions per skill and printable answer keys.',
            'list_sep' => ', ', 'paren' => ' (%s)', 'topics_all' => 'Topics across all %s', 'pages4' => '4 pages',
            'subj_title' => 'Free %1$s Worksheets %2$s (%3$s)', 'subj_h1' => '%s Worksheets', 'browse_topic' => 'Browse by topic',
            'country_title' => 'Free %1$s Worksheets (%2$s)', 'country_h1' => '%s Worksheets',
            'topic_ws' => '%1$s worksheets: %2$s',
            'pin_unit' => 'Free %1$s %2$s %3$s worksheet: short lesson, 100 practice questions and a printable answer key.',
            'date_fmt' => 'F j, Y',
            'pr_title' => '%1$s %2$s Worksheet with Answer Key (Printable, %3$s)',
            'pr_desc' => 'Free printable %1$s %2$s worksheet%3$s: %4$d questions on 3 pages plus an answer key. Print it or save it as a PDF.',
            'pr_h' => '%1$s Worksheet (%2$s)', 'pr_pin' => 'Free printable %1$s %2$s worksheet with answer key.',
            'pv_brand' => '%s Worksheets', 'pv_cta_unit' => 'FREE · Lesson + 100 questions + answer key',
            'pv_cta_grade' => 'FREE · %d printable worksheets', 'pv_cta_topic' => 'FREE · %d skills with answer keys',
            'pv_skills' => '%d skills', 'pv_100each' => '100 questions each', 'pv_keys' => 'Answer keys',
            'pv_lesson' => 'Lesson', 'pv_lessons' => 'Lessons', 'pv_100' => '100 questions', 'pv_print' => 'Printable %s',
            'pv_key' => 'Answer key', 'pv_practice' => 'Practice · %s',
            'pv_name1' => 'Name ______________   Date ________', 'pv_name2' => 'Name ____________________    Date __________',
            'pv_foot' => 'Free · apu2.com/worksheets',
        ),
        // Taiwan: Traditional Chinese (台灣用語)
        'zh-TW' => array(
            'home' => '學習單', 'grades' => '年級', 'units' => '單元',
            'questions' => '題', 'points' => '重點', 'quiz100' => '100題練習',
            'quiz_lead' => '共5回、每回20題。作答後馬上知道答案和解說。',
            'learn_quiz' => '重點＋100題', 'print' => '列印', 'pdf' => 'PDF',
            'your_score' => '你的成績', 'clear_grade' => '清除這個年級的成績',
            'hook_title' => '100題練習', 'hook_sub' => '每回20題・共5回・馬上對答案',
            'hook_go' => '開始練習', 'faq' => '常見問題',
            'related' => '繼續學習', 'prev' => '上一個', 'next_u' => '下一個',
            'all_units' => '全部單元：', 'printable_of' => '可列印的學習單（附解答）',
            'standard' => '課綱', 'updated' => '更新', 'by' => '製作',
            'pick_grade' => '選擇年級', 'pick_subject' => '選擇科目',
            'print_sheets' => '可列印的學習單',
            'print_note' => '共4頁：暖身、練習1、練習2、解答',
            'print_btn' => '列印／存成PDF', 'pdf_btn' => '下載PDF',
            'lesson_link' => '重點說明與線上練習',
            'p_warmup' => '暖身', 'p_prac1' => '練習1', 'p_prac2' => '練習2',
            'p_key' => '解答', 'name' => '姓名', 'date' => '日期', 'score' => '得分',
            'circle' => '請圈出正確答案的號碼。', 'total_q' => '共%d題',
            'for_check' => '對答案用',
            'license' => '可免費列印、影印，供家庭與教室使用。',
            'worksheets' => '學習單', 'grade_ws' => '%s%s學習單',
            'notfound' => '找不到這個頁面', 'back_home' => '回到全部學習單',
            'skills_count' => '%d個單元', 'free' => '免費・免註冊',
            'by_grade' => '依年級', 'pin_save' => '存到 Pinterest',
            'grade_title_sfx' => '｜免費下載列印＋線上練習',
            'grade_desc' => '%1$s%2$s免費學習單，依照%3$s編排：%4$s。每個單元100題練習，附可列印的解答。',
            'list_sep' => '、', 'paren' => '（%s）', 'topics_all' => '各%s的主題', 'pages4' => '4頁',
            'subj_title' => '%1$s學習單｜%2$s免費下載（%3$s）', 'subj_h1' => '%s學習單', 'browse_topic' => '依主題找',
            'country_title' => '%1$s免費學習單（%2$s）', 'country_h1' => '%s學習單',
            'topic_ws' => '%1$s學習單：%2$s',
            'pin_unit' => '免費%1$s%2$s「%3$s」學習單：重點說明、100題練習、可列印的解答。',
            'date_fmt' => 'Y年n月j日',
            'pr_title' => '%1$s「%2$s」學習單（附解答・%3$s列印）',
            'pr_desc' => '免費列印的%1$s「%2$s」學習單%3$s：3頁共%4$d題，最後一頁是解答。可以直接列印或存成PDF。',
            'pr_h' => '%1$s學習單（%2$s）', 'pr_pin' => '免費列印的%1$s「%2$s」學習單（附解答）',
            'pv_brand' => '%s 學習單', 'pv_cta_unit' => '免費・重點說明＋100題＋解答',
            'pv_cta_grade' => '免費・%d份可列印學習單', 'pv_cta_topic' => '免費・%d個單元（附解答）',
            'pv_skills' => '%d個單元', 'pv_100each' => '每單元100題', 'pv_keys' => '附解答',
            'pv_lesson' => '重點說明', 'pv_lessons' => '重點說明', 'pv_100' => '100題', 'pv_print' => '%s列印',
            'pv_key' => '附解答', 'pv_practice' => '練習・%s',
            'pv_name1' => '姓名 ______________   日期 ________', 'pv_name2' => '姓名 ____________________    日期 __________',
            'pv_foot' => '免費・apu2.com/worksheets',
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
    if (!isset($T['en-SG'])) $T['en-SG'] = array_merge($T['en-GB'], array(   // Singapore: British spelling, Primary 1-6 levels
        'grades' => 'Levels', 'pick_grade' => 'Choose a level', 'clear_grade' => 'Clear scores for this level', 'by_grade' => 'by Level',
    ));
    if (!isset($T['en-CA'])) $T['en-CA'] = array_merge($T['en'], array('hook_go' => 'Start practising'));   // Canada: grades like the US, British -ise verbs
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
            'ranks' => 'Ranks', 'moreAfter' => 'More ranks after {t}', 'unlocksAfter' => 'unlocks after {t}', 'reached' => 'Reached', 'toGoShort' => '{n} to go', 'you' => 'You',
            'how' => '1 lap = every {name} question answered correctly once ({n} answers). Each skill counts up to the lap you are on, so keep every skill going.',
            'levelUp' => 'Level up!', 'keepGoing' => 'Keep going to {t}', 'yay' => 'Awesome',
            'achieved' => 'Goal reached!', 'ask' => 'Go for <b>{t}</b> next ({l})?',
            'goFor' => 'Go for it', 'later' => 'Later', 'notStarted' => 'Not started',
        ),
    );
    $J['zh-TW'] = array(
            'ok' => '答對了！', 'ng' => '再想想', 'ans' => '答案：', 'next' => '下一題',
            'result' => '看結果', 'done' => '完成', 'practice' => '練習',
            'score' => '答對 <b>{o}</b> 題（共 {n} 題）', 'best' => '最高紀錄：{o} / {t}',
            'm100' => '全部答對！可以挑戰下一回了。',
            'm80' => '差一點點！把答錯的題目再做一次。',
            'mlow' => '先看看上面的例題，再挑戰一次這一回。',
            'redoMiss' => '只重做答錯的 {n} 題', 'redoAll' => '從頭再做一次',
            'loadErr' => '題目載入失敗。', 'notYet' => '還沒開始',
            'total' => '答對 <b>{o}</b> / {t} 題', 'mastered' => '（全對的單元 {c} / {u}）',
            'confirm' => '要清除這個年級的全部成績嗎？',
            'hook0' => '還沒開始。先從第1回（20題）開始吧。',
            'hookAll' => '5回全部答對！隨時回來複習。',
            'hookSome' => '已全對 {d} / {n} 回，再 {r} 回就完成了！',
            'okWords' => array('答對了！', '很棒！', '太厲害了！', '好樣的！', '做得好！'),
            'ngWords' => array('差一點！', '下一題加油！', '繼續努力！'),
            'streak' => array('3' => '連對3題！', '5' => '連對5題！', '10' => '連對10題！',
                              '15' => '連對15題！', '20' => '整回全對！'),
            'perfect' => '滿分！', 'good' => '做得很好！',
            'tier' => array('above' => '高於平均', 'sight' => '前段班在望', 'class' => '班上第一',
                            'grade' => '年級第一', 'state' => '縣市第一',
                            'nation' => '全國第一', 'world' => '世界第一'),
            'start' => '起點', 'yourRank' => '你的{name}等級', 'rankOf' => '{name}等級',
            'correct' => '題答對', 'todayPlus' => '今天 +{n}',
            'more' => '再答對 <b>{n}</b> 題就到「{t}」',
            'toGo' => '再 {n} 題到「{t}」', 'reachedBtn' => '達成了！看下一個目標',
            'allDone' => '所有等級都達成了！', 'lap' => '第{n}輪', 'laps' => '第{n}輪',
            'ranks' => '等級', 'moreAfter' => '「{t}」之後還有更多等級', 'unlocksAfter' => '「{t}」之後開放', 'reached' => '已達成', 'toGoShort' => '還差 {n} 題', 'you' => '你',
            'how' => '1輪 = {name}的每一題都答對一次（共 {n} 題）。每個單元最多算到你目前的輪數，所以每個單元都要練習喔。',
            'levelUp' => '升級了！', 'keepGoing' => '繼續朝「{t}」前進', 'yay' => '太棒了',
            'achieved' => '目標達成！', 'ask' => '下一個目標挑戰「<b>{t}</b>」嗎？（{l}）',
            'goFor' => '挑戰', 'later' => '之後再說', 'notStarted' => '還沒開始',
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
    $J['en-SG'] = array_merge($J['en'], array(
        'confirm' => 'Clear all saved scores for this level?',
        'tier' => array('above' => 'Above Average', 'sight' => 'Top in Sight', 'class' => 'Top of the Class',
                        'grade' => 'Top of the Level', 'state' => 'Top of the School',
                        'nation' => 'Top in Singapore', 'world' => 'Top in the World'),
    ));
    $J['en-CA'] = array_merge($J['en'], array(
        'tier' => array('above' => 'Above Average', 'sight' => 'Top in Sight', 'class' => 'Top of the Class',
                        'grade' => 'Top of the Grade', 'state' => 'Top in the Province',
                        'nation' => 'Top in the Country', 'world' => 'Top in the World'),
    ));
    return isset($J[$lang]) ? $J[$lang] : $J['en'];
}

/* ---------------------------------------------------------------- layout */
function page_head($o) {
    // $o: lang, title, desc, canonical(path), og_type, hreflang, body_class, noindex, image(path)
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
    if (!empty($o['image'])) {                       // preview picture (inc/preview.php)
        $img = abs_url($o['image']);
        echo '<meta property="og:image" content="' . h($img) . "\">\n";
        echo "<meta property=\"og:image:width\" content=\"1200\">\n<meta property=\"og:image:height\" content=\"630\">\n";
        echo '<meta property="og:image:alt" content="' . h($o['title']) . "\">\n";
        echo "<meta name=\"twitter:card\" content=\"summary_large_image\">\n";
        echo '<meta name="twitter:image" content="' . h($img) . "\">\n";
    } else {
        echo "<meta name=\"twitter:card\" content=\"summary\">\n";
    }
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
/* "Save to Pinterest" link for a page: the tall pin.png picture, the page URL and a short description.
   A plain link (no Pinterest script), so nothing is loaded until someone clicks it. */
function pin_link($page_path, $desc, $class = 'ws-pin') {
    $img = preview_path($page_path);
    if (!$img) return '';
    $href = 'https://www.pinterest.com/pin/create/button/?url=' . rawurlencode(abs_url($page_path))
          . '&media=' . rawurlencode(abs_url(preg_replace('#preview\.png$#', 'pin.png', $img)))
          . '&description=' . rawurlencode($desc);
    return '<a class="' . $class . '" href="' . h($href) . '" target="_blank" rel="noopener nofollow">'
         . '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a6.5 6.5 0 0 0-6.5 6.5c0 4.6 6.5 13.5 6.5 13.5s6.5-8.9 6.5-13.5A6.5 6.5 0 0 0 12 2zm0 9a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>' . h(T('pin_save')) . '</a>';
}

/* path of the preview picture for a page path ('' when this server cannot draw it) */
function preview_path($page_path) {
    static $ok = null;
    if ($ok === null) $ok = function_exists('imagecreatetruecolor') && function_exists('imagettftext');
    return $ok ? rtrim($page_path, '/') . '/preview.png' : '';
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
