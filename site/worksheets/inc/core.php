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
            'topic_ws' => '%1$s worksheets: %2$s', 'topic_h1' => '%s Worksheets',
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
            'topic_ws' => '%1$s學習單：%2$s', 'topic_h1' => '%s學習單',
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
        // Germany: German (Grundschule)
        'de' => array(
            'home' => 'Arbeitsblätter', 'grades' => 'Klassen', 'units' => 'Themen',
            'questions' => 'Aufgaben', 'points' => 'Das Wichtigste', 'quiz100' => '100 Übungsaufgaben',
            'quiz_lead' => '5 Runden mit je 20 Aufgaben. Du siehst sofort die Lösung und einen Tipp.',
            'learn_quiz' => 'Erklärung + 100 Aufgaben', 'print' => 'Drucken', 'pdf' => 'PDF',
            'your_score' => 'Dein Ergebnis', 'clear_grade' => 'Ergebnisse dieser Klasse löschen',
            'hook_title' => '100 Übungsaufgaben', 'hook_sub' => '5 Runden mit je 20 · sofort Rückmeldung',
            'hook_go' => 'Jetzt üben', 'faq' => 'Häufige Fragen',
            'related' => 'Weiterlernen', 'prev' => 'Zurück', 'next_u' => 'Weiter',
            'all_units' => 'Alle Themen:', 'printable_of' => 'Arbeitsblatt zum Ausdrucken mit Lösungen',
            'standard' => 'Bildungsstandards', 'updated' => 'Aktualisiert am', 'by' => 'Von',
            'pick_grade' => 'Klasse wählen', 'pick_subject' => 'Fach wählen',
            'print_sheets' => 'Arbeitsblätter zum Ausdrucken',
            'print_note' => '4 Seiten: Aufwärmen, Übung 1, Übung 2, Lösungen',
            'print_btn' => 'Drucken / als PDF speichern', 'pdf_btn' => 'PDF herunterladen',
            'lesson_link' => 'Erklärung und Online-Übung',
            'p_warmup' => 'Aufwärmen', 'p_prac1' => 'Übung 1', 'p_prac2' => 'Übung 2',
            'p_key' => 'Lösungen', 'name' => 'Name', 'date' => 'Datum', 'score' => 'Punkte',
            'circle' => 'Kreise die Nummer der richtigen Antwort ein.', 'total_q' => '%d Aufgaben',
            'for_check' => 'Zum Kontrollieren',
            'license' => 'Kostenlos zum Ausdrucken und Kopieren für zu Hause und den Unterricht.',
            'worksheets' => 'Arbeitsblätter', 'grade_ws' => '%2$s %1$s Arbeitsblätter',
            'notfound' => 'Seite nicht gefunden', 'back_home' => 'Zurück zu allen Arbeitsblättern',
            'skills_count' => '%d Themen', 'free' => 'Kostenlos · ohne Anmeldung',
            'by_grade' => 'nach Klassen', 'pin_save' => 'Auf Pinterest merken',
            'grade_title_sfx' => ': kostenlos ausdrucken + online üben',
            'grade_desc' => 'Kostenlose %2$s-Arbeitsblätter für die %1$s nach den %3$s: %4$s. 100 Übungsaufgaben pro Thema und Lösungen zum Ausdrucken.',
            'list_sep' => ', ', 'paren' => ' (%s)', 'topics_all' => 'Themen über alle %s', 'pages4' => '4 Seiten',
            'subj_title' => 'Kostenlose %1$s-Arbeitsblätter %2$s (%3$s)', 'subj_h1' => '%s-Arbeitsblätter', 'browse_topic' => 'Nach Themen suchen',
            'country_title' => 'Kostenlose Arbeitsblätter für %1$s (%2$s)', 'country_h1' => 'Arbeitsblätter für %s',
            'topic_ws' => '%1$s: Arbeitsblätter (%2$s)', 'topic_h1' => '%s: Arbeitsblätter',
            'pin_unit' => '%2$s %1$s, %3$s: kostenloses Arbeitsblatt mit kurzer Erklärung, 100 Übungsaufgaben und Lösungen.',
            'date_fmt' => 'd.m.Y',
            'pr_title' => '%2$s %1$s: Arbeitsblatt mit Lösungen (zum Ausdrucken, %3$s)',
            'pr_desc' => 'Kostenloses Arbeitsblatt zum Ausdrucken: %2$s, %1$s%3$s. %4$d Aufgaben auf 3 Seiten und ein Lösungsblatt. Direkt ausdrucken oder als PDF speichern.',
            'pr_h' => 'Arbeitsblatt: %1$s (%2$s)', 'pr_pin' => 'Kostenloses Arbeitsblatt zum Ausdrucken: %2$s, %1$s, mit Lösungen.',
            'pv_brand' => '%s Arbeitsblätter', 'pv_cta_unit' => 'KOSTENLOS · Erklärung + 100 Aufgaben + Lösungen',
            'pv_cta_grade' => 'KOSTENLOS · %d Arbeitsblätter zum Ausdrucken', 'pv_cta_topic' => 'KOSTENLOS · %d Themen mit Lösungen',
            'pv_skills' => '%d Themen', 'pv_100each' => 'je 100 Aufgaben', 'pv_keys' => 'Lösungen',
            'pv_lesson' => 'Erklärung', 'pv_lessons' => 'Erklärungen', 'pv_100' => '100 Aufgaben', 'pv_print' => 'Druckvorlage %s',
            'pv_key' => 'Lösungen', 'pv_practice' => 'Übung · %s',
            'pv_name1' => 'Name ______________   Datum ________', 'pv_name2' => 'Name ____________________    Datum __________',
            'pv_foot' => 'Kostenlos · apu2.com/worksheets',
            'gs' => '%2$s %1$s', 'lc' => 'keep', 'range' => '%1$s bis %2$s',
        ),
        // France: French (école élémentaire)
        'fr' => array(
            'home' => 'Fiches', 'grades' => 'Classes', 'units' => 'Notions',
            'questions' => 'exercices', 'points' => 'L’essentiel', 'quiz100' => '100 exercices',
            'quiz_lead' => '5 séries de 20 exercices. Tu vois tout de suite la réponse et une explication.',
            'learn_quiz' => 'Leçon + 100 exercices', 'print' => 'Imprimer', 'pdf' => 'PDF',
            'your_score' => 'Ton score', 'clear_grade' => 'Effacer les scores de cette classe',
            'hook_title' => '100 exercices', 'hook_sub' => '5 séries de 20 · correction immédiate',
            'hook_go' => 'Commencer', 'faq' => 'Questions fréquentes',
            'related' => 'Pour continuer', 'prev' => 'Précédent', 'next_u' => 'Suivant',
            'all_units' => 'Toutes les notions :', 'printable_of' => 'Fiche à imprimer avec corrigé',
            'standard' => 'Programme', 'updated' => 'Mis à jour le', 'by' => 'Par',
            'pick_grade' => 'Choisir une classe', 'pick_subject' => 'Choisir une matière',
            'print_sheets' => 'Fiches à imprimer',
            'print_note' => '4 pages : échauffement, exercices 1, exercices 2, corrigé',
            'print_btn' => 'Imprimer / enregistrer en PDF', 'pdf_btn' => 'Télécharger le PDF',
            'lesson_link' => 'Leçon et exercices en ligne', 'colon' => '&nbsp;:',
            'p_warmup' => 'Échauffement', 'p_prac1' => 'Exercices 1', 'p_prac2' => 'Exercices 2',
            'p_key' => 'Corrigé', 'name' => 'Prénom', 'date' => 'Date', 'score' => 'Score',
            'circle' => 'Entoure le numéro de la bonne réponse.', 'total_q' => '%d exercices',
            'for_check' => 'Pour corriger',
            'license' => 'Gratuit à imprimer et à photocopier pour la maison et la classe.',
            'worksheets' => 'Fiches', 'grade_ws' => 'Fiches de %2$s %1$s',
            'notfound' => 'Page introuvable', 'back_home' => 'Retour à toutes les fiches',
            'skills_count' => '%d notions', 'free' => 'Gratuit · sans inscription',
            'by_grade' => 'par classe', 'pin_save' => 'Enregistrer sur Pinterest',
            'grade_title_sfx' => ' : fiches gratuites à imprimer + exercices en ligne',
            'grade_desc' => 'Fiches de %2$s gratuites pour le %1$s, conformes aux %3$s : %4$s. 100 exercices par notion et un corrigé à imprimer.',
            'list_sep' => ', ', 'paren' => ' (%s)', 'topics_all' => 'Thèmes sur toutes les %s', 'pages4' => '4 pages',
            'subj_title' => 'Fiches de %1$s gratuites %2$s (%3$s)', 'subj_h1' => 'Fiches de %s', 'browse_topic' => 'Chercher par thème',
            'country_title' => 'Fiches gratuites pour la %1$s (%2$s)', 'country_h1' => 'Fiches pour la %s',
            'topic_ws' => '%1$s : fiches (%2$s)', 'topic_h1' => '%s : fiches et exercices',
            'pin_unit' => 'Fiche gratuite de %2$s %1$s, %3$s : leçon courte, 100 exercices et corrigé.',
            'date_fmt' => 'd/m/Y',
            'pr_title' => 'Fiche %1$s, %2$s : exercices avec corrigé (à imprimer, %3$s)',
            'pr_desc' => 'Fiche gratuite à imprimer : %2$s, %1$s%3$s. %4$d exercices sur 3 pages et une page de corrigé. À imprimer directement ou à enregistrer en PDF.',
            'pr_h' => 'Fiche : %1$s (%2$s)', 'pr_pin' => 'Fiche gratuite à imprimer : %2$s, %1$s, avec corrigé.',
            'pv_brand' => 'Fiches %s', 'pv_cta_unit' => 'GRATUIT · leçon + 100 exercices + corrigé',
            'pv_cta_grade' => 'GRATUIT · %d fiches à imprimer', 'pv_cta_topic' => 'GRATUIT · %d notions avec corrigé',
            'pv_skills' => '%d notions', 'pv_100each' => '100 exercices chacune', 'pv_keys' => 'corrigés',
            'pv_lesson' => 'Leçon', 'pv_lessons' => 'Leçons', 'pv_100' => '100 exercices', 'pv_print' => 'Fiche %s',
            'pv_key' => 'Corrigé', 'pv_practice' => 'Exercices · %s',
            'pv_name1' => 'Prénom ______________   Date ________', 'pv_name2' => 'Prénom ____________________    Date __________',
            'pv_foot' => 'Gratuit · apu2.com/worksheets',
            'gs' => '%2$s %1$s', 'range' => 'du %1$s au %2$s',
        ),
        // Brazil: Brazilian Portuguese (Ensino Fundamental, BNCC)
        'pt-BR' => array(
            'home' => 'Atividades', 'grades' => 'Anos', 'units' => 'Conteúdos',
            'questions' => 'exercícios', 'points' => 'Resumo', 'quiz100' => '100 exercícios',
            'quiz_lead' => '5 séries de 20 exercícios. Você vê na hora a resposta certa e a explicação.',
            'learn_quiz' => 'Aula + 100 exercícios', 'print' => 'Imprimir', 'pdf' => 'PDF',
            'your_score' => 'Sua pontuação', 'clear_grade' => 'Apagar as pontuações deste ano',
            'hook_title' => '100 exercícios', 'hook_sub' => '5 séries de 20 · correção na hora',
            'hook_go' => 'Começar', 'faq' => 'Perguntas frequentes',
            'related' => 'Para continuar', 'prev' => 'Anterior', 'next_u' => 'Próximo',
            'all_units' => 'Todos os conteúdos:', 'printable_of' => 'Atividade para imprimir com gabarito',
            'standard' => 'BNCC', 'updated' => 'Atualizado em', 'by' => 'Por',
            'pick_grade' => 'Escolha o ano', 'pick_subject' => 'Escolha a matéria',
            'print_sheets' => 'Atividades para imprimir',
            'print_note' => '4 páginas: aquecimento, exercícios 1, exercícios 2, gabarito',
            'print_btn' => 'Imprimir / salvar em PDF', 'pdf_btn' => 'Baixar o PDF',
            'lesson_link' => 'Aula e exercícios on-line',
            'p_warmup' => 'Aquecimento', 'p_prac1' => 'Exercícios 1', 'p_prac2' => 'Exercícios 2',
            'p_key' => 'Gabarito', 'name' => 'Nome', 'date' => 'Data', 'score' => 'Acertos',
            'circle' => 'Circule o número da resposta certa.', 'total_q' => '%d exercícios',
            'for_check' => 'Para corrigir',
            'license' => 'Grátis para imprimir e copiar para uso em casa e na escola.',
            'worksheets' => 'Atividades', 'grade_ws' => '%2$s – %1$s',
            'notfound' => 'Página não encontrada', 'back_home' => 'Voltar para todas as atividades',
            'skills_count' => '%d conteúdos', 'free' => 'Grátis · sem cadastro',
            'by_grade' => 'por ano', 'pin_save' => 'Salvar no Pinterest',
            'grade_title_sfx' => ': atividades grátis para imprimir + exercícios on-line',
            'grade_desc' => 'Atividades de %2$s grátis para o %1$s, de acordo com a %3$s: %4$s. 100 exercícios por conteúdo e gabarito para imprimir.',
            'list_sep' => ', ', 'paren' => ' (%s)', 'topics_all' => 'Temas em todos os %s', 'pages4' => '4 páginas',
            'subj_title' => 'Atividades de %1$s grátis %2$s (%3$s)', 'subj_h1' => 'Atividades de %s', 'browse_topic' => 'Procurar por tema',
            'country_title' => 'Atividades grátis para o %1$s (%2$s)', 'country_h1' => 'Atividades para o %s',
            'topic_ws' => '%1$s: atividades (%2$s)', 'topic_h1' => '%s: atividades e exercícios',
            'pin_unit' => 'Atividade grátis de %2$s, %1$s, %3$s: aula curta, 100 exercícios e gabarito.',
            'date_fmt' => 'd/m/Y',
            'pr_title' => 'Atividade %1$s, %2$s: exercícios com gabarito (para imprimir, %3$s)',
            'pr_desc' => 'Atividade grátis para imprimir: %2$s, %1$s%3$s. %4$d exercícios em 3 páginas e uma página de gabarito. Imprima direto ou salve em PDF.',
            'pr_h' => 'Atividade: %1$s (%2$s)', 'pr_pin' => 'Atividade grátis para imprimir: %2$s, %1$s, com gabarito.',
            'pv_brand' => 'Atividades %s', 'pv_cta_unit' => 'GRÁTIS · aula + 100 exercícios + gabarito',
            'pv_cta_grade' => 'GRÁTIS · %d atividades para imprimir', 'pv_cta_topic' => 'GRÁTIS · %d conteúdos com gabarito',
            'pv_skills' => '%d conteúdos', 'pv_100each' => '100 exercícios cada', 'pv_keys' => 'gabaritos',
            'pv_lesson' => 'Aula', 'pv_lessons' => 'Aulas', 'pv_100' => '100 exercícios', 'pv_print' => 'Atividade %s',
            'pv_key' => 'Gabarito', 'pv_practice' => 'Exercícios · %s',
            'pv_name1' => 'Nome ______________   Data ________', 'pv_name2' => 'Nome ____________________    Data __________',
            'pv_foot' => 'Grátis · apu2.com/worksheets',
            'gs' => '%2$s %1$s', 'range' => 'do %1$s ao %2$s',
        ),
        // Italy: Italian (scuola primaria)
        'it' => array(
            'home' => 'Schede', 'grades' => 'Classi', 'units' => 'Argomenti',
            'questions' => 'esercizi', 'points' => 'In breve', 'quiz100' => '100 esercizi',
            'quiz_lead' => '5 serie da 20 esercizi. Vedi subito la risposta giusta e la spiegazione.',
            'learn_quiz' => 'Lezione + 100 esercizi', 'print' => 'Stampa', 'pdf' => 'PDF',
            'your_score' => 'Il tuo punteggio', 'clear_grade' => 'Cancella i punteggi di questa classe',
            'hook_title' => '100 esercizi', 'hook_sub' => '5 serie da 20 · correzione immediata',
            'hook_go' => 'Inizia', 'faq' => 'Domande frequenti',
            'related' => 'Per continuare', 'prev' => 'Precedente', 'next_u' => 'Successivo',
            'all_units' => 'Tutti gli argomenti:', 'printable_of' => 'Scheda da stampare con soluzioni',
            'standard' => 'Indicazioni nazionali', 'updated' => 'Aggiornato il', 'by' => 'Di',
            'pick_grade' => 'Scegli una classe', 'pick_subject' => 'Scegli una materia',
            'print_sheets' => 'Schede da stampare',
            'print_note' => '4 pagine: riscaldamento, esercizi 1, esercizi 2, soluzioni',
            'print_btn' => 'Stampa / salva in PDF', 'pdf_btn' => 'Scarica il PDF',
            'lesson_link' => 'Lezione ed esercizi online',
            'p_warmup' => 'Riscaldamento', 'p_prac1' => 'Esercizi 1', 'p_prac2' => 'Esercizi 2',
            'p_key' => 'Soluzioni', 'name' => 'Nome', 'date' => 'Data', 'score' => 'Punteggio',
            'circle' => 'Cerchia il numero della risposta giusta.', 'total_q' => '%d esercizi',
            'for_check' => 'Per correggere',
            'license' => 'Gratis da stampare e fotocopiare per la casa e la classe.',
            'worksheets' => 'Schede', 'grade_ws' => 'Schede di %2$s %1$s',
            'notfound' => 'Pagina non trovata', 'back_home' => 'Torna a tutte le schede',
            'skills_count' => '%d argomenti', 'free' => 'Gratis · senza registrazione',
            'by_grade' => 'per classe', 'pin_save' => 'Salva su Pinterest',
            'grade_title_sfx' => ': schede gratis da stampare + esercizi online',
            'grade_desc' => 'Schede di %2$s gratis per la %1$s, secondo le %3$s: %4$s. 100 esercizi per argomento e le soluzioni da stampare.',
            'list_sep' => ', ', 'paren' => ' (%s)', 'topics_all' => 'Argomenti di tutte le %s', 'pages4' => '4 pagine',
            'subj_title' => 'Schede di %1$s gratis %2$s (%3$s)', 'subj_h1' => 'Schede di %s', 'browse_topic' => 'Cerca per argomento',
            'country_title' => 'Schede gratis per l’%1$s (%2$s)', 'country_h1' => 'Schede per l’%s',
            'topic_ws' => '%1$s: schede (%2$s)', 'topic_h1' => '%s: schede ed esercizi',
            'pin_unit' => 'Scheda gratis di %2$s %1$s, %3$s: lezione breve, 100 esercizi e soluzioni.',
            'date_fmt' => 'd/m/Y',
            'pr_title' => 'Scheda %1$s, %2$s: esercizi con soluzioni (da stampare, %3$s)',
            'pr_desc' => 'Scheda gratis da stampare: %2$s, %1$s%3$s. %4$d esercizi su 3 pagine e una pagina di soluzioni. Da stampare subito o salvare in PDF.',
            'pr_h' => 'Scheda: %1$s (%2$s)', 'pr_pin' => 'Scheda gratis da stampare: %2$s, %1$s, con soluzioni.',
            'pv_brand' => 'Schede %s', 'pv_cta_unit' => 'GRATIS · lezione + 100 esercizi + soluzioni',
            'pv_cta_grade' => 'GRATIS · %d schede da stampare', 'pv_cta_topic' => 'GRATIS · %d argomenti con soluzioni',
            'pv_skills' => '%d argomenti', 'pv_100each' => '100 esercizi ciascuno', 'pv_keys' => 'soluzioni',
            'pv_lesson' => 'Lezione', 'pv_lessons' => 'Lezioni', 'pv_100' => '100 esercizi', 'pv_print' => 'Scheda %s',
            'pv_key' => 'Soluzioni', 'pv_practice' => 'Esercizi · %s',
            'pv_name1' => 'Nome ______________   Data ________', 'pv_name2' => 'Nome ____________________    Data __________',
            'pv_foot' => 'Gratis · apu2.com/worksheets',
            'gs' => '%2$s %1$s', 'range' => 'dalla %1$s alla %2$s',
        ),
        // Spain: Spanish (Educación Primaria, LOMLOE)
        'es' => array(
            'home' => 'Fichas', 'grades' => 'Cursos', 'units' => 'Temas',
            'questions' => 'ejercicios', 'points' => 'En resumen', 'quiz100' => '100 ejercicios',
            'quiz_lead' => '5 series de 20 ejercicios. Ves al momento la respuesta correcta y la explicación.',
            'learn_quiz' => 'Lección + 100 ejercicios', 'print' => 'Imprimir', 'pdf' => 'PDF',
            'your_score' => 'Tu puntuación', 'clear_grade' => 'Borrar las puntuaciones de este curso',
            'hook_title' => '100 ejercicios', 'hook_sub' => '5 series de 20 · corrección al momento',
            'hook_go' => 'Empezar', 'faq' => 'Preguntas frecuentes',
            'related' => 'Para seguir', 'prev' => 'Anterior', 'next_u' => 'Siguiente',
            'all_units' => 'Todos los temas:', 'printable_of' => 'Ficha para imprimir con soluciones',
            'standard' => 'LOMLOE', 'updated' => 'Actualizado el', 'by' => 'Por',
            'pick_grade' => 'Elige un curso', 'pick_subject' => 'Elige una asignatura',
            'print_sheets' => 'Fichas para imprimir',
            'print_note' => '4 páginas: calentamiento, ejercicios 1, ejercicios 2, soluciones',
            'print_btn' => 'Imprimir / guardar en PDF', 'pdf_btn' => 'Descargar el PDF',
            'lesson_link' => 'Lección y ejercicios en línea',
            'p_warmup' => 'Calentamiento', 'p_prac1' => 'Ejercicios 1', 'p_prac2' => 'Ejercicios 2',
            'p_key' => 'Soluciones', 'name' => 'Nombre', 'date' => 'Fecha', 'score' => 'Aciertos',
            'circle' => 'Rodea el número de la respuesta correcta.', 'total_q' => '%d ejercicios',
            'for_check' => 'Para corregir',
            'license' => 'Gratis para imprimir y fotocopiar en casa y en el aula.',
            'worksheets' => 'Fichas', 'grade_ws' => 'Fichas de %2$s de %1$s',
            'notfound' => 'Página no encontrada', 'back_home' => 'Volver a todas las fichas',
            'skills_count' => '%d temas', 'free' => 'Gratis · sin registro',
            'by_grade' => 'por curso', 'pin_save' => 'Guardar en Pinterest',
            'grade_title_sfx' => ': fichas gratis para imprimir + ejercicios en línea',
            'grade_desc' => 'Fichas de %2$s gratis para %1$s, según la %3$s: %4$s. 100 ejercicios por tema y soluciones para imprimir.',
            'list_sep' => ', ', 'paren' => ' (%s)', 'topics_all' => 'Temas de todos los %s', 'pages4' => '4 páginas',
            'subj_title' => 'Fichas de %1$s gratis %2$s (%3$s)', 'subj_h1' => 'Fichas de %s', 'browse_topic' => 'Buscar por tema',
            'country_title' => 'Fichas gratis para %1$s (%2$s)', 'country_h1' => 'Fichas para %s',
            'topic_ws' => '%1$s: fichas (%2$s)', 'topic_h1' => '%s: fichas y ejercicios',
            'pin_unit' => 'Ficha gratis de %2$s de %1$s, %3$s: lección breve, 100 ejercicios y soluciones.',
            'date_fmt' => 'd/m/Y',
            'pr_title' => 'Ficha de %2$s, %1$s: ejercicios con soluciones (para imprimir, %3$s)',
            'pr_desc' => 'Ficha gratis para imprimir: %2$s, %1$s%3$s. %4$d ejercicios en 3 páginas y una página de soluciones. Imprímela directamente o guárdala en PDF.',
            'pr_h' => 'Ficha: %1$s (%2$s)', 'pr_pin' => 'Ficha gratis para imprimir: %2$s, %1$s, con soluciones.',
            'pv_brand' => 'Fichas %s', 'pv_cta_unit' => 'GRATIS · lección + 100 ejercicios + soluciones',
            'pv_cta_grade' => 'GRATIS · %d fichas para imprimir', 'pv_cta_topic' => 'GRATIS · %d temas con soluciones',
            'pv_skills' => '%d temas', 'pv_100each' => '100 ejercicios cada uno', 'pv_keys' => 'soluciones',
            'pv_lesson' => 'Lección', 'pv_lessons' => 'Lecciones', 'pv_100' => '100 ejercicios', 'pv_print' => 'Ficha %s',
            'pv_key' => 'Soluciones', 'pv_practice' => 'Ejercicios · %s',
            'pv_name1' => 'Nombre ______________   Fecha ________', 'pv_name2' => 'Nombre ____________________    Fecha __________',
            'pv_foot' => 'Gratis · apu2.com/worksheets',
            'gs' => '%2$s de %1$s', 'range' => 'de %1$s a %2$s',
        ),
        // Korea: Korean (2022 개정 교육과정)
        'ko' => array(
            'home' => '학습지', 'grades' => '학년', 'units' => '단원',
            'questions' => '문제', 'points' => '핵심 정리', 'quiz100' => '100문제 연습',
            'quiz_lead' => '5회, 회마다 20문제. 답을 고르면 바로 정답과 풀이를 볼 수 있어요.',
            'learn_quiz' => '개념 + 100문제', 'print' => '인쇄', 'pdf' => 'PDF',
            'your_score' => '내 점수', 'clear_grade' => '이 학년의 점수 지우기',
            'hook_title' => '100문제 연습', 'hook_sub' => '20문제 × 5회 · 바로 채점',
            'hook_go' => '연습 시작', 'faq' => '자주 묻는 질문',
            'related' => '이어서 공부하기', 'prev' => '이전', 'next_u' => '다음',
            'all_units' => '전체 단원:', 'printable_of' => '인쇄용 학습지(정답 포함)',
            'standard' => '교육과정', 'updated' => '업데이트', 'by' => '만든 곳',
            'pick_grade' => '학년 선택', 'pick_subject' => '과목 선택',
            'print_sheets' => '인쇄용 학습지',
            'print_note' => '4쪽: 준비 문제, 연습 1, 연습 2, 정답',
            'print_btn' => '인쇄 / PDF로 저장', 'pdf_btn' => 'PDF 내려받기',
            'lesson_link' => '개념 정리와 온라인 연습',
            'p_warmup' => '준비 문제', 'p_prac1' => '연습 1', 'p_prac2' => '연습 2',
            'p_key' => '정답', 'name' => '이름', 'date' => '날짜', 'score' => '점수',
            'circle' => '알맞은 답의 번호에 ○표 하세요.', 'total_q' => '%d문제',
            'for_check' => '채점용',
            'license' => '가정과 교실에서 무료로 인쇄하고 복사할 수 있습니다.',
            'worksheets' => '학습지', 'grade_ws' => '%s %s 학습지',
            'notfound' => '페이지를 찾을 수 없습니다', 'back_home' => '전체 학습지로 돌아가기',
            'skills_count' => '%d개 단원', 'free' => '무료 · 회원 가입 없음',
            'by_grade' => '학년별', 'pin_save' => 'Pinterest에 저장',
            'grade_title_sfx' => ' | 무료 인쇄 학습지 + 온라인 연습',
            'grade_desc' => '%1$s %2$s 무료 학습지. %3$s에 맞춘 단원: %4$s. 단원마다 100문제와 인쇄용 정답이 있습니다.',
            'list_sep' => ', ', 'paren' => ' (%s)', 'topics_all' => '모든 %s의 주제', 'pages4' => '4쪽',
            'subj_title' => '%1$s 학습지 | %2$s 무료 (%3$s)', 'subj_h1' => '%s 학습지', 'browse_topic' => '주제별로 찾기',
            'country_title' => '%1$s 무료 학습지 (%2$s)', 'country_h1' => '%s 학습지',
            'topic_ws' => '%1$s 학습지: %2$s', 'topic_h1' => '%s 학습지',
            'pin_unit' => '무료 %1$s %2$s 「%3$s」 학습지: 개념 정리, 100문제, 인쇄용 정답.',
            'date_fmt' => 'Y년 n월 j일',
            'pr_title' => '%1$s 「%2$s」 학습지 (정답 포함 · %3$s 인쇄)',
            'pr_desc' => '무료로 인쇄하는 %1$s 「%2$s」 학습지%3$s: 3쪽 %4$d문제와 정답 1쪽. 바로 인쇄하거나 PDF로 저장할 수 있습니다.',
            'pr_h' => '%1$s 학습지 (%2$s)', 'pr_pin' => '무료 인쇄 %1$s 「%2$s」 학습지 (정답 포함)',
            'pv_brand' => '%s 학습지', 'pv_cta_unit' => '무료 · 개념 정리 + 100문제 + 정답',
            'pv_cta_grade' => '무료 · 인쇄용 학습지 %d개', 'pv_cta_topic' => '무료 · %d개 단원 (정답 포함)',
            'pv_skills' => '%d개 단원', 'pv_100each' => '단원마다 100문제', 'pv_keys' => '정답 포함',
            'pv_lesson' => '개념 정리', 'pv_lessons' => '개념 정리', 'pv_100' => '100문제', 'pv_print' => '%s 인쇄',
            'pv_key' => '정답 포함', 'pv_practice' => '연습 · %s',
            'pv_name1' => '이름 ______________   날짜 ________', 'pv_name2' => '이름 ____________________    날짜 __________',
            'pv_foot' => '무료 · apu2.com/worksheets',
            'lc' => 'keep', 'range' => '%1$s ~ %2$s',
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
    if (!isset($T['es-MX'])) $T['es-MX'] = array_merge($T['es'], array(   // México: grados, respuestas, programa de la SEP
        'grades' => 'Grados', 'pick_grade' => 'Elige un grado', 'clear_grade' => 'Borrar las puntuaciones de este grado', 'by_grade' => 'por grado',
        'standard' => 'Programa SEP', 'p_key' => 'Respuestas', 'pv_key' => 'Respuestas', 'pv_keys' => 'respuestas',
        'circle' => 'Encierra en un círculo el número de la respuesta correcta.', 'printable_of' => 'Ficha para imprimir con respuestas',
        'license' => 'Gratis para imprimir y fotocopiar en casa y en el salón de clases.',
        'grade_desc' => 'Fichas de %2$s gratis para %1$s, según la %3$s: %4$s. 100 ejercicios por tema y respuestas para imprimir.',
        'pin_unit' => 'Ficha gratis de %2$s de %1$s, %3$s: lección breve, 100 ejercicios y respuestas.',
        'pr_title' => 'Ficha de %2$s, %1$s: ejercicios con respuestas (para imprimir, %3$s)',
        'pr_pin' => 'Ficha gratis para imprimir: %2$s, %1$s, con respuestas.',
        'pv_cta_unit' => 'GRATIS · lección + 100 ejercicios + respuestas', 'pv_cta_topic' => 'GRATIS · %d temas con respuestas',
        'pr_desc' => 'Ficha gratis para imprimir: %2$s, %1$s%3$s. %4$d ejercicios en 3 páginas y una página de respuestas. Imprímela directamente o guárdala en PDF.',
        'date_fmt' => 'd/m/Y',
    ));
    if (!isset($T['en-CA'])) $T['en-CA'] = array_merge($T['en'], array('hook_go' => 'Start practising'));   // Canada: grades like the US, British -ise verbs
    static $lang = 'en';
    if (is_array($key)) { $lang = isset($T[$key[0]]) ? $key[0] : 'en'; return null; } // set language
    if ($key === null) return $T[$lang];
    return isset($T[$lang][$key]) ? $T[$lang][$key] : $key;
}

/* Korean particle after a word: ko_josa('분수', '은', '는') -> '분수는' (batchim decides) */
function ko_josa($w, $with, $without) {
    $c = mb_substr(preg_replace('/[^\x{AC00}-\x{D7A3}0-9A-Za-z]+$/u', '', $w), -1);
    if ($c === '') return $w . $without;
    $o = mb_ord($c);
    if ($o >= 0xAC00 && $o <= 0xD7A3) $has = (($o - 0xAC00) % 28) !== 0;
    else $has = strpos('013678LMNlmn', $c) !== false;   // 영, 일, 삼, 육, 칠, 팔 / -l, -m, -n
    return $w . ($has ? $with : $without);
}

/* "Grade 3 Math" / "Mathe Klasse 3": grade and subject in the order of the page language */
function gs($grade, $subject) {
    $f = T('gs');
    return sprintf($f === 'gs' ? '%1$s %2$s' : $f, $grade, $subject);
}
/* lower case inside an English sentence ("grade 3 math worksheets"); German nouns keep their capital */
function lc($s) { return T('lc') === 'keep' ? $s : strtolower($s); }

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
    $J['de'] = array(
            'ok' => 'Richtig!', 'ng' => 'Noch nicht', 'ans' => 'Lösung:', 'next' => 'Weiter',
            'result' => 'Ergebnis ansehen', 'done' => 'Fertig', 'practice' => 'Üben',
            'score' => '<b>{o}</b> von {n} richtig', 'best' => 'Dein bestes Ergebnis: {o} / {t}',
            'm100' => 'Alles richtig! Du bist bereit für die nächste Runde.',
            'm80' => 'Fast geschafft. Rechne nur die falschen Aufgaben noch einmal.',
            'mlow' => 'Lies dir die Beispiele oben durch und versuche diese Runde noch einmal.',
            'redoMiss' => 'Die {n} falschen noch einmal', 'redoAll' => 'Von vorne beginnen',
            'loadErr' => 'Die Aufgaben konnten nicht geladen werden.', 'notYet' => 'Noch nicht begonnen',
            'total' => '<b>{o}</b> / {t} richtig', 'mastered' => '({c} / {u} Themen geschafft)',
            'confirm' => 'Alle gespeicherten Ergebnisse dieser Klasse löschen?',
            'hook0' => 'Noch nicht begonnen. Fang mit Runde 1 an (20 Aufgaben).',
            'hookAll' => 'Alle 5 Runden geschafft! Komm jederzeit zum Wiederholen zurück.',
            'hookSome' => '{d} von {n} Runden geschafft. Noch {r}!',
            'okWords' => array('Richtig!', 'Super!', 'Toll gemacht!', 'Genau!', 'Prima!'),
            'ngWords' => array('Fast!', 'Probier die nächste!', 'Weiter so!'),
            'streak' => array('3' => '3 richtig in Folge!', '5' => '5 richtig in Folge!', '10' => '10 richtig in Folge!',
                              '15' => '15 richtig in Folge!', '20' => 'Runde ohne Fehler!'),
            'perfect' => 'Alles richtig!', 'good' => 'Gut gemacht!',
            'tier' => array('above' => 'Über dem Durchschnitt', 'sight' => 'Spitze in Sicht', 'class' => 'Klassenbeste',
                            'grade' => 'Jahrgangsbeste', 'state' => 'Landesspitze',
                            'nation' => 'Bundesspitze', 'world' => 'Weltspitze'),
            'start' => 'Start', 'yourRank' => 'Dein Rang in {name}', 'rankOf' => 'Rang in {name}',
            'correct' => 'richtige Antworten', 'todayPlus' => 'heute +{n}',
            'more' => 'Noch <b>{n}</b> richtige Antworten bis {t}',
            'toGo' => 'Noch {n} bis {t}', 'reachedBtn' => 'Geschafft! Nächstes Ziel ansehen',
            'allDone' => 'Du hast alle Ränge erreicht!', 'lap' => '{n} Runde', 'laps' => '{n} Runden',
            'ranks' => 'Ränge', 'moreAfter' => 'Weitere Ränge nach {t}', 'unlocksAfter' => 'ab {t} freigeschaltet', 'reached' => 'Erreicht', 'toGoShort' => 'noch {n}', 'you' => 'Du',
            'how' => '1 Runde = jede Aufgabe in {name} einmal richtig gelöst ({n} Antworten). Jedes Thema zählt bis zur Runde, in der du gerade bist. Übe also alle Themen.',
            'levelUp' => 'Aufgestiegen!', 'keepGoing' => 'Weiter bis {t}', 'yay' => 'Klasse',
            'achieved' => 'Ziel erreicht!', 'ask' => 'Als Nächstes <b>{t}</b> schaffen ({l})?',
            'goFor' => 'Los geht\'s', 'later' => 'Später', 'notStarted' => 'Noch nicht begonnen',
            'sep' => '.',
    );
    $J['fr'] = array(
            'ok' => 'Bravo !', 'ng' => 'Pas encore', 'ans' => 'Réponse :', 'next' => 'Suivant',
            'result' => 'Voir le résultat', 'done' => 'Terminé', 'practice' => 'S’entraîner',
            'score' => '<b>{o}</b> sur {n} justes', 'best' => 'Ton meilleur score : {o} / {t}',
            'm100' => 'Tout est juste ! Tu peux passer à la série suivante.',
            'm80' => 'Presque ! Refais seulement les exercices ratés.',
            'mlow' => 'Relis les exemples ci-dessus, puis refais cette série.',
            'redoMiss' => 'Refaire les {n} exercices ratés', 'redoAll' => 'Tout recommencer',
            'loadErr' => 'Impossible de charger les exercices.', 'notYet' => 'Pas encore commencé',
            'total' => '<b>{o}</b> / {t} justes', 'mastered' => '({c} / {u} notions réussies)',
            'confirm' => 'Effacer tous les scores enregistrés pour cette classe ?',
            'hook0' => 'Pas encore commencé. Commence par la série 1 (20 exercices).',
            'hookAll' => 'Les 5 séries sont réussies ! Reviens quand tu veux pour réviser.',
            'hookSome' => '{d} séries réussies sur {n}. Encore {r} !',
            'okWords' => array('Bravo !', 'Super !', 'Bien joué !', 'Exact !', 'Très bien !'),
            'ngWords' => array('Presque !', 'Essaie la suivante !', 'Continue !'),
            'streak' => array('3' => '3 de suite !', '5' => '5 de suite !', '10' => '10 de suite !',
                              '15' => '15 de suite !', '20' => 'Série parfaite !'),
            'perfect' => 'Tout est juste !', 'good' => 'Bon travail !',
            'tier' => array('above' => 'Au-dessus de la moyenne', 'sight' => 'Le sommet est proche', 'class' => 'Premier de la classe',
                            'grade' => 'Premier du niveau', 'state' => 'Premier de la région',
                            'nation' => 'Premier de France', 'world' => 'Premier du monde'),
            'start' => 'Départ', 'yourRank' => 'Ton rang en {name}', 'rankOf' => 'Rang en {name}',
            'correct' => 'bonnes réponses', 'todayPlus' => 'aujourd’hui +{n}',
            'more' => 'Encore <b>{n}</b> bonnes réponses pour atteindre {t}',
            'toGo' => 'Encore {n} pour {t}', 'reachedBtn' => 'Atteint ! Voir le prochain objectif',
            'allDone' => 'Tu as atteint tous les rangs !', 'lap' => '{n} tour', 'laps' => '{n} tours',
            'ranks' => 'Rangs', 'moreAfter' => 'D’autres rangs après {t}', 'unlocksAfter' => 'débloqué après {t}', 'reached' => 'Atteint', 'toGoShort' => 'encore {n}', 'you' => 'Toi',
            'how' => '1 tour = chaque exercice de {name} réussi une fois ({n} réponses). Chaque notion compte jusqu’au tour où tu en es : entraîne-toi donc sur toutes les notions.',
            'levelUp' => 'Niveau supérieur !', 'keepGoing' => 'Continue jusqu’à {t}', 'yay' => 'Génial',
            'achieved' => 'Objectif atteint !', 'ask' => 'Prochain objectif : <b>{t}</b> ({l}) ?',
            'goFor' => 'C’est parti', 'later' => 'Plus tard', 'notStarted' => 'Pas encore commencé',
            'sep' => ' ',
    );
    $J['pt-BR'] = array(
            'ok' => 'Muito bem!', 'ng' => 'Ainda não', 'ans' => 'Resposta:', 'next' => 'Próximo',
            'result' => 'Ver o resultado', 'done' => 'Terminou', 'practice' => 'Praticar',
            'score' => '<b>{o}</b> acertos de {n}', 'best' => 'Seu recorde: {o} / {t}',
            'm100' => 'Acertou tudo! Pode ir para a próxima série.',
            'm80' => 'Quase! Refaça só os exercícios que errou.',
            'mlow' => 'Releia os exemplos acima e refaça esta série.',
            'redoMiss' => 'Refazer os {n} exercícios errados', 'redoAll' => 'Recomeçar tudo',
            'loadErr' => 'Não foi possível carregar os exercícios.', 'notYet' => 'Ainda não começou',
            'total' => '<b>{o}</b> / {t} acertos', 'mastered' => '({c} / {u} conteúdos concluídos)',
            'confirm' => 'Apagar todas as pontuações salvas deste ano?',
            'hook0' => 'Ainda não começou. Comece pela série 1 (20 exercícios).',
            'hookAll' => 'Você terminou as 5 séries! Volte quando quiser para revisar.',
            'hookSome' => '{d} de {n} séries concluídas. Faltam {r}!',
            'okWords' => array('Muito bem!', 'Ótimo!', 'Isso!', 'Certo!', 'Excelente!'),
            'ngWords' => array('Quase!', 'Tente a próxima!', 'Continue assim!'),
            'streak' => array('3' => '3 seguidas!', '5' => '5 seguidas!', '10' => '10 seguidas!',
                              '15' => '15 seguidas!', '20' => 'Série perfeita!'),
            'perfect' => 'Acertou tudo!', 'good' => 'Bom trabalho!',
            'tier' => array('above' => 'Acima da média', 'sight' => 'O topo está perto', 'class' => 'Melhor da turma',
                            'grade' => 'Melhor do ano', 'state' => 'Melhor do estado',
                            'nation' => 'Melhor do Brasil', 'world' => 'Melhor do mundo'),
            'start' => 'Largada', 'yourRank' => 'Seu nível em {name}', 'rankOf' => 'Nível em {name}',
            'correct' => 'acertos', 'todayPlus' => 'hoje +{n}',
            'more' => 'Faltam <b>{n}</b> acertos para chegar a {t}',
            'toGo' => 'Faltam {n} para {t}', 'reachedBtn' => 'Conseguiu! Ver o próximo objetivo',
            'allDone' => 'Você chegou a todos os níveis!', 'lap' => '{n} volta', 'laps' => '{n} voltas',
            'ranks' => 'Níveis', 'moreAfter' => 'Mais níveis depois de {t}', 'unlocksAfter' => 'libera depois de {t}', 'reached' => 'Conseguiu', 'toGoShort' => 'faltam {n}', 'you' => 'Você',
            'how' => '1 volta = acertar uma vez cada exercício de {name} ({n} respostas). Cada conteúdo conta até a volta em que você chegou: por isso, pratique todos os conteúdos.',
            'levelUp' => 'Subiu de nível!', 'keepGoing' => 'Continue até {t}', 'yay' => 'Demais',
            'achieved' => 'Objetivo alcançado!', 'ask' => 'Próximo objetivo: <b>{t}</b> ({l})?',
            'goFor' => 'Vamos lá', 'later' => 'Depois', 'notStarted' => 'Ainda não começou',
            'sep' => '.',
    );
    $J['es'] = array(
            'ok' => '¡Muy bien!', 'ng' => 'Todavía no', 'ans' => 'Respuesta:', 'next' => 'Siguiente',
            'result' => 'Ver el resultado', 'done' => 'Terminado', 'practice' => 'Practicar',
            'score' => '<b>{o}</b> aciertos de {n}', 'best' => 'Tu récord: {o} / {t}',
            'm100' => '¡Todo bien! Puedes pasar a la siguiente serie.',
            'm80' => '¡Casi! Repite solo los ejercicios que fallaste.',
            'mlow' => 'Vuelve a leer los ejemplos de arriba y repite esta serie.',
            'redoMiss' => 'Repetir los {n} ejercicios fallados', 'redoAll' => 'Empezar de nuevo',
            'loadErr' => 'No se han podido cargar los ejercicios.', 'notYet' => 'Todavía no has empezado',
            'total' => '<b>{o}</b> / {t} aciertos', 'mastered' => '({c} / {u} temas terminados)',
            'confirm' => '¿Borrar todas las puntuaciones guardadas de este curso?',
            'hook0' => 'Todavía no has empezado. Empieza por la serie 1 (20 ejercicios).',
            'hookAll' => '¡Has terminado las 5 series! Vuelve cuando quieras para repasar.',
            'hookSome' => '{d} de {n} series terminadas. ¡Faltan {r}!',
            'okWords' => array('¡Muy bien!', '¡Genial!', '¡Eso es!', '¡Correcto!', '¡Excelente!'),
            'ngWords' => array('¡Casi!', '¡A por la siguiente!', '¡Sigue así!'),
            'streak' => array('3' => '¡3 seguidas!', '5' => '¡5 seguidas!', '10' => '¡10 seguidas!',
                              '15' => '¡15 seguidas!', '20' => '¡Serie perfecta!'),
            'perfect' => '¡Todo bien!', 'good' => '¡Buen trabajo!',
            'tier' => array('above' => 'Por encima de la media', 'sight' => 'La cima está cerca', 'class' => 'El mejor de la clase',
                            'grade' => 'El mejor del curso', 'state' => 'El mejor de la comunidad',
                            'nation' => 'El mejor de España', 'world' => 'El mejor del mundo'),
            'start' => 'Salida', 'yourRank' => 'Tu nivel en {name}', 'rankOf' => 'Nivel en {name}',
            'correct' => 'aciertos', 'todayPlus' => 'hoy +{n}',
            'more' => 'Faltan <b>{n}</b> aciertos para llegar a {t}',
            'toGo' => 'Faltan {n} para {t}', 'reachedBtn' => '¡Conseguido! Ver el siguiente objetivo',
            'allDone' => '¡Has llegado a todos los niveles!', 'lap' => '{n} vuelta', 'laps' => '{n} vueltas',
            'ranks' => 'Niveles', 'moreAfter' => 'Más niveles después de {t}', 'unlocksAfter' => 'se desbloquea después de {t}', 'reached' => 'Conseguido', 'toGoShort' => 'faltan {n}', 'you' => 'Tú',
            'how' => '1 vuelta = acertar una vez cada ejercicio de {name} ({n} respuestas). Cada tema cuenta hasta la vuelta a la que has llegado: por eso, practica todos los temas.',
            'levelUp' => '¡Has subido de nivel!', 'keepGoing' => 'Sigue hasta {t}', 'yay' => '¡Genial!',
            'achieved' => '¡Objetivo conseguido!', 'ask' => '¿Siguiente objetivo: <b>{t}</b> ({l})?',
            'goFor' => '¡Vamos!', 'later' => 'Luego', 'notStarted' => 'Todavía no has empezado',
            'sep' => ' ',
    );
    $J['it'] = array(
            'ok' => 'Bravo!', 'ng' => 'Non ancora', 'ans' => 'Risposta:', 'next' => 'Avanti',
            'result' => 'Vedi il risultato', 'done' => 'Finito', 'practice' => 'Esercitati',
            'score' => '<b>{o}</b> giuste su {n}', 'best' => 'Il tuo record: {o} / {t}',
            'm100' => 'Tutto giusto! Puoi passare alla serie successiva.',
            'm80' => 'Quasi! Rifai solo gli esercizi sbagliati.',
            'mlow' => 'Rileggi gli esempi qui sopra, poi rifai questa serie.',
            'redoMiss' => 'Rifai i {n} esercizi sbagliati', 'redoAll' => 'Ricomincia tutto',
            'loadErr' => 'Impossibile caricare gli esercizi.', 'notYet' => 'Non ancora iniziato',
            'total' => '<b>{o}</b> / {t} giuste', 'mastered' => '({c} / {u} argomenti completati)',
            'confirm' => 'Cancellare tutti i punteggi salvati per questa classe?',
            'hook0' => 'Non ancora iniziato. Comincia dalla serie 1 (20 esercizi).',
            'hookAll' => 'Hai completato tutte e 5 le serie! Torna quando vuoi per ripassare.',
            'hookSome' => '{d} serie completate su {n}. Ne mancano {r}!',
            'okWords' => array('Bravo!', 'Ottimo!', 'Esatto!', 'Giusto!', 'Benissimo!'),
            'ngWords' => array('Quasi!', 'Prova la prossima!', 'Continua così!'),
            'streak' => array('3' => '3 di fila!', '5' => '5 di fila!', '10' => '10 di fila!',
                              '15' => '15 di fila!', '20' => 'Serie perfetta!'),
            'perfect' => 'Tutto giusto!', 'good' => 'Buon lavoro!',
            'tier' => array('above' => 'Sopra la media', 'sight' => 'La vetta è vicina', 'class' => 'Primo della classe',
                            'grade' => 'Primo dell’anno', 'state' => 'Primo della regione',
                            'nation' => 'Primo d’Italia', 'world' => 'Primo del mondo'),
            'start' => 'Partenza', 'yourRank' => 'Il tuo livello in {name}', 'rankOf' => 'Livello in {name}',
            'correct' => 'risposte giuste', 'todayPlus' => 'oggi +{n}',
            'more' => 'Ancora <b>{n}</b> risposte giuste per arrivare a {t}',
            'toGo' => 'Ancora {n} per {t}', 'reachedBtn' => 'Raggiunto! Vedi il prossimo obiettivo',
            'allDone' => 'Hai raggiunto tutti i livelli!', 'lap' => '{n} giro', 'laps' => '{n} giri',
            'ranks' => 'Livelli', 'moreAfter' => 'Altri livelli dopo {t}', 'unlocksAfter' => 'si sblocca dopo {t}', 'reached' => 'Raggiunto', 'toGoShort' => 'ancora {n}', 'you' => 'Tu',
            'how' => '1 giro = ogni esercizio di {name} fatto giusto una volta ({n} risposte). Ogni argomento conta fino al giro a cui sei arrivato: esercitati quindi su tutti gli argomenti.',
            'levelUp' => 'Livello superiore!', 'keepGoing' => 'Continua fino a {t}', 'yay' => 'Fantastico',
            'achieved' => 'Obiettivo raggiunto!', 'ask' => 'Prossimo obiettivo: <b>{t}</b> ({l})?',
            'goFor' => 'Andiamo', 'later' => 'Più tardi', 'notStarted' => 'Non ancora iniziato',
            'sep' => ' ',
    );
    $J['ko'] = array(
            'ok' => '정답!', 'ng' => '다시 생각해 봐요', 'ans' => '정답: ', 'next' => '다음 문제',
            'result' => '결과 보기', 'done' => '끝', 'practice' => '연습',
            'score' => '{n}문제 중 <b>{o}</b>문제 정답', 'best' => '최고 기록: {o} / {t}',
            'm100' => '모두 맞혔어요! 다음 회에 도전해 보세요.',
            'm80' => '조금만 더! 틀린 문제를 다시 풀어 보세요.',
            'mlow' => '위의 예제를 다시 읽고 이 회에 한 번 더 도전해 보세요.',
            'redoMiss' => '틀린 {n}문제만 다시 풀기', 'redoAll' => '처음부터 다시 풀기',
            'loadErr' => '문제를 불러오지 못했습니다.', 'notYet' => '아직 시작 전',
            'total' => '<b>{o}</b> / {t}문제 정답', 'mastered' => '(모두 맞힌 단원 {c} / {u})',
            'confirm' => '이 학년에 저장된 점수를 모두 지울까요?',
            'hook0' => '아직 시작하지 않았어요. 1회(20문제)부터 시작해 보세요.',
            'hookAll' => '5회 모두 만점! 언제든지 다시 복습하세요.',
            'hookSome' => '{n}회 중 {d}회 만점. {r}회만 더 하면 끝!',
            'okWords' => array('정답!', '잘했어요!', '대단해요!', '훌륭해요!', '멋져요!'),
            'ngWords' => array('아깝다!', '다음 문제는 할 수 있어요!', '힘내요!'),
            'streak' => array('3' => '3문제 연속 정답!', '5' => '5문제 연속 정답!', '10' => '10문제 연속 정답!',
                              '15' => '15문제 연속 정답!', '20' => '한 회 모두 정답!'),
            'perfect' => '만점!', 'good' => '아주 잘했어요!',
            'tier' => array('above' => '평균 이상', 'sight' => '상위권이 눈앞', 'class' => '반에서 1등',
                            'grade' => '학년에서 1등', 'state' => '시·도에서 1등',
                            'nation' => '전국 1등', 'world' => '세계 1등'),
            'start' => '출발', 'yourRank' => '나의 {name} 등급', 'rankOf' => '{name} 등급',
            'correct' => '문제 정답', 'todayPlus' => '오늘 +{n}',
            'more' => '<b>{n}</b>문제 더 맞히면 「{t}」',
            'toGo' => '「{t}」까지 {n}문제', 'reachedBtn' => '달성! 다음 목표 보기',
            'allDone' => '모든 등급을 달성했어요!', 'lap' => '{n}바퀴', 'laps' => '{n}바퀴',
            'ranks' => '등급', 'moreAfter' => '「{t}」 다음에도 등급이 더 있어요', 'unlocksAfter' => '「{t}」 다음에 열려요', 'reached' => '달성', 'toGoShort' => '{n}문제 남음', 'you' => '나',
            'how' => '1바퀴 = {name}의 모든 문제를 한 번씩 맞히기(모두 {n}문제). 단원마다 지금 바퀴 수까지만 세니까 모든 단원을 골고루 연습하세요.',
            'levelUp' => '등급 상승!', 'keepGoing' => '다음 목표 「{t}」까지 계속', 'yay' => '좋아요',
            'achieved' => '목표 달성!', 'ask' => '다음 목표 「<b>{t}</b>」에 도전할까요? ({l})',
            'goFor' => '도전', 'later' => '나중에', 'notStarted' => '아직 시작 전',
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
    $J['es-MX'] = array_merge($J['es'], array(
        'confirm' => '¿Borrar todas las puntuaciones guardadas de este grado?',
        'ngWords' => array('¡Casi!', '¡Vamos por la siguiente!', '¡Sigue así!'),
        'tier' => array('above' => 'Por encima del promedio', 'sight' => 'La cima está cerca', 'class' => 'El mejor del salón',
                        'grade' => 'El mejor del grado', 'state' => 'El mejor del estado',
                        'nation' => 'El mejor de México', 'world' => 'El mejor del mundo'),
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
/* The curriculum a grade follows: usually the country's, but Korean kindergarten follows the 누리과정 */
function grade_standard($country, $grade) {
    if ($country['code'] === 'kr' && $grade && $grade['slug'] === 'kindergarten') return '2019 개정 누리과정';
    return $country['standard'];
}
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
