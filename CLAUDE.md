# Aplus worksheets（apu2.com/worksheets/）

各国の学習指導要領に沿った、無料のレッスン＋100問クイズ＋印刷用プリント（4ページ）。
ページは PHP が DB から作る動的ページ。**静的HTMLは作らない**（ロリポップのファイル数上限のため）。

## 仕組み

| 場所 | 中身 | 本番への反映 |
|------|------|-------------|
| `site/worksheets/` | PHP・CSS・JS（ページの型枠） | GitHub Actions が FTP で `/aplus/worksheets/` へ |
| `content/catalog.json` | 国・教科・学年 | Actions が `api/sync.php` 経由で DB（ws_country / ws_subject / ws_grade） |
| `content/{国}/{教科}/{学年}/{単元}.json` | 1単元のレッスン・問題 | Actions が DB の ws_unit へ（変わった単元だけ） |
| `tools/gen_*.py` | 単元JSONを作る生成スクリプト | （実行してJSONをコミットする） |
| `tools/check.py` | 公開前チェック | Actions が毎回実行。エラーなら止まる |

main に push すると `.github/workflows/deploy.yml` が「チェック → FTP → DB更新」を自動で行う。
FTP は上書きのみ（`--delete` を絶対に付けない）。DB は ws_ の4テーブルへの REPLACE だけ（DELETE・DROP・ALTER を書かない）。

## 「次の単元」と言われたら

1. 下のロードマップで、まだ `content/` に無い最初の単元を選ぶ
2. `tools/gen_{国}_{教科}_{学年}_{単元}.py` を新しく作る（既存の `gen_us_math_g3_time.py` などと同じ形）
   - 出力: `content/{国}/{教科}/{学年}/{slug}.json`
   - `random.Random(固定の数)` を使い、何度実行しても同じ問題になるようにする
3. `python3 tools/gen_....py` を実行
4. `python3 tools/check.py` がエラー0・警告0になるまで直す
5. 生成スクリプトとJSONを **main に直接コミット**して push（ブランチ・PRは作らない）
   - メッセージ例: `Add us/math/grade-3/perimeter (3.MD.D.8)`
6. ユーザーには短く日本語で、作った単元と確認URLを伝える
   - 例: https://www.apu2.com/worksheets/us/math/grade-3/perimeter/

## トピック別ページとプレビュー画像（毎回あわせて強くする）

- トピック別ページ `/{国}/{教科}/topics/{topic}/` は `site/worksheets/inc/topics.php` の正規表現（単元 slug に一致）で自動で集まる。3単元以上で公開
- 新しい単元を作ったら、どのトピックに入るか確認する（`unit_topic_slugs()`）。どれにも入らない・違うトピックに入るときは `in`/`out` の正規表現を直す
- 新しい分野が3単元以上たまったら、`topic_defs()` に新しいトピックを足す（name・blurb、英国式は name_gb/blurb_gb）
- プレビュー画像 `.../preview.png`（1200×630、og:image・サイトマップ）は単元・学年・トピックで自動。ファイルは作らない（毎回 PHP の GD で描く）
- 新しい国は `topic_gb()`（英国式の綴り）と core.php の UI 文言を確認する

## 単元JSONの形

```json
{
  "country": "us", "subject": "math", "grade": "grade-3", "slug": "perimeter",
  "title": "H1", "seo_title": "<title>", "short_title": "Perimeter",
  "domain": "学年ページでのグループ見出し（例: Measurement & Data）",
  "standard_code": "3.MD.D.8", "standard_url": "...", "standard_text": "基準の原文",
  "meta_desc": "...", "key_big": "一番大事な考え（大きく表示）", "key_sub": "補足",
  "body_html": "レッスン本文のHTML", "faq": [{"q": "...", "a": "..."}],
  "sets": [ {"title": "セット名", "items": [ {"q": "問題HTML", "c": ["4つの選択肢"], "a": 0, "e": "解説"} ] } ],
  "pdf_url": "", "sort": 7, "updated": "YYYY-MM-DD"
}
```

- セットは **5つ、各20問**（合計100問）。易しい → 難しい の順。最後は文章題
- `sort` は学年ページでの並び順。既存の最大値＋1
- HTML の属性は **シングルクォート**、バックスラッシュ禁止（`check.py` で検出）
- 図は inline SVG（`viewBox='0 0 W H'` を必ず付ける）。時計など正方形の図は印刷で大きく出る
- 分数は `<span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>`

## 品質ルール（学習者に分かりやすく、正確に）

- 誤答は「よくある間違い」から作る（適当な数字にしない）
- 英語の文法を確認: `1 minute`（複数形にしない）、`p.m.` の後に `.` を重ねない、人名と代名詞の一致
- 場面と数値を現実に合わせる（登校は朝、映画は夜、9:60 のような時刻を作らない）
- 同じ問題を繰り返さない。答えが0になる問題（9:00 to 9:00）を作らない
- `body_html` は「考え方 → 例 → よくある間違い」の順で、短い文で
- 絵文字は使わない（必要ならSVG）

## ロードマップ（効果の高い順）

US / Math / Grade 3（Common Core）
1. multiplication-facts ✓ 2. division-facts ✓ 3. rounding ✓ 4. fractions ✓ 5. telling-time ✓ 6. area ✓
7. perimeter ✓
8. add-subtract-within-1000 ✓
9. two-step-word-problems ✓
10. picture-and-bar-graphs ✓
11. line-plots-measurement ✓
12. quadrilaterals ✓
13. mass-and-volume ✓
14. multiply-by-multiples-of-10 ✓
15. properties-of-multiplication ✓
16. partition-shapes ✓

US / Math / Grade 4（Common Core）
1. multi-digit-multiplication ✓
2. long-division ✓
3. equivalent-fractions ✓
4. compare-fractions ✓
5. add-subtract-fractions ✓
6. multiply-fractions-by-whole-numbers ✓
7. decimals-tenths-hundredths ✓
8. place-value-rounding ✓
9. add-subtract-multi-digit ✓
10. factors-multiples-prime ✓
11. multiplicative-comparison-word-problems ✓
12. measurement-conversions ✓
13. area-perimeter-formulas ✓
14. measuring-angles ✓
15. lines-angles-shapes ✓
16. line-symmetry ✓
17. number-shape-patterns ✓
18. line-plots-fractions ✓

Grade 4 からは 1,000 以上の数にカンマを付ける（例: 4,536）。

US / Math / Grade 2（Common Core）— 1000 まで（カンマなし。Grade 3 と同じ）。文は短く、7〜8歳が読める英語で
1. addition-subtraction-facts ✓
2. add-subtract-within-100 ✓
3. word-problems-within-100 ✓
4. place-value ✓
5. counting-money ✓
6. telling-time-5-minutes ✓
7. add-subtract-within-1000 ✓
8. compare-three-digit-numbers ✓
9. skip-counting ✓
10. odd-and-even ✓
11. arrays-repeated-addition ✓
12. measuring-length ✓
13. length-word-problems ✓
14. graphs-and-line-plots ✓
15. shapes-and-attributes ✓
16. halves-thirds-fourths ✓

US / Math / Grade 5（Common Core）— 1,000 以上はカンマ付き
1. add-subtract-fractions-unlike ✓
2. multiply-fractions ✓
3. divide-fractions ✓
4. add-subtract-decimals ✓
5. multiply-divide-decimals ✓
6. volume ✓
7. numerical-expressions ✓
8. coordinate-plane ✓
9. multi-digit-multiplication ✓
10. long-division-two-digit-divisors ✓
11. decimal-place-value-rounding ✓
12. fractions-as-division ✓
13. multiplication-as-scaling ✓
14. measurement-conversions ✓
15. classify-two-dimensional-figures ✓
16. patterns-and-relationships ✓
17. line-plots-fractions ✓

US / Math / Grade 6（Common Core）— 1,000 以上はカンマ付き。負の数は「−」（U+2212）
1. ratios ✓
2. unit-rates ✓
3. ratio-tables ✓
4. percents ✓
5. divide-fractions-by-fractions ✓
6. gcf-and-lcm ✓
7. negative-numbers ✓
8. exponents-order-of-operations ✓
9. one-step-equations ✓
10. writing-evaluating-expressions ✓
11. equivalent-expressions ✓
12. area-of-polygons ✓
13. absolute-value-and-ordering ✓
14. coordinate-plane-four-quadrants ✓
15. inequalities ✓
16. mean-median-mode-range ✓
17. surface-area-nets ✓
18. volume-fractional-edges ✓
19. decimal-operations ✓
20. converting-units-with-ratios ✓

US / Math / Grade 1（Common Core）— 120 まで（カンマなし）。文はとても短く、6〜7歳が読める英語で。絵（SVG）を多く
1. addition-subtraction-within-20 ✓
2. word-problems-within-20 ✓
3. add-three-numbers ✓
4. place-value-tens-ones ✓
5. count-to-120 ✓
6. compare-two-digit-numbers ✓
7. add-within-100 ✓
8. ten-more-ten-less ✓
9. subtract-multiples-of-10 ✓
10. telling-time-hour-half-hour ✓
11. measuring-length ✓
12. equal-sign-missing-numbers ✓
13. addition-subtraction-strategies ✓
14. organize-data ✓
15. shapes-and-attributes ✓
16. halves-and-fourths ✓

UK / Maths / Year 4（National Curriculum in England）— country `uk`、subject `maths`、grade `year-N`、A4。
イギリス英語（colour, metre, maths, pupils, £/p, trapezium, exchange）。1,000 以上はカンマ。standard_code は「Year 4: 分野名」
1. times-tables ✓
2. place-value ✓
3. rounding ✓
4. roman-numerals ✓
5. column-addition-and-subtraction ✓
6. mental-multiplication-and-division ✓
7. short-multiplication ✓
8. fractions ✓
9. decimals ✓
10. money ✓
11. converting-units ✓
12. area-and-perimeter ✓
13. time-12-and-24-hour-clock ✓
14. angles-and-shapes ✓
15. lines-of-symmetry ✓
16. coordinates ✓
17. bar-charts-and-time-graphs ✓

UK / Maths / Year 6（KS2 SATs の学年）— Year 4 と同じルール
1. place-value-and-rounding ✓
2. long-multiplication ✓
3. long-division ✓
4. order-of-operations ✓
5. factors-multiples-and-primes ✓
6. simplifying-and-comparing-fractions ✓
7. adding-and-subtracting-fractions ✓
8. multiplying-and-dividing-fractions ✓
9. fractions-decimals-and-percentages ✓
10. decimal-calculations ✓
11. percentages-of-amounts ✓
12. ratio-and-proportion ✓
13. algebra ✓
14. converting-units ✓
15. area-perimeter-and-volume ✓
16. angles ✓
17. circles-and-nets ✓
18. coordinates-and-transformations ✓
19. pie-charts-and-line-graphs ✓
20. mean ✓

UK / Maths / Year 5 — Year 4 と同じルール
1. place-value-to-a-million ✓
2. rounding ✓
3. roman-numerals-to-1000 ✓
4. column-addition-and-subtraction ✓
5. factors-multiples-and-primes ✓
6. multiplication ✓
7. short-division ✓
8. multiply-and-divide-by-10-100-1000 ✓
9. equivalent-fractions-and-mixed-numbers ✓
10. adding-and-subtracting-fractions ✓
11. multiplying-fractions ✓
12. decimals-and-percentages ✓
13. converting-units ✓
14. area-and-perimeter ✓
15. measuring-angles ✓
16. reflection-and-translation ✓
17. line-graphs-and-tables ✓

UK / Maths / Year 3 — 1,000 まで。文は短く、絵を多く
1. place-value ✓
2. mental-addition-and-subtraction ✓
3. column-addition-and-subtraction ✓
4. 3-4-and-8-times-tables ✓
5. multiplication-and-division ✓
6. fractions ✓
7. tenths-and-adding-fractions ✓
8. measuring-length-mass-and-capacity ✓
9. perimeter ✓
10. money ✓
11. telling-the-time ✓
12. angles-and-lines ✓
13. 2d-and-3d-shapes ✓
14. bar-charts-and-pictograms ✓

UK / Maths / Year 2（KS1）— 100 まで。文はとても短く、絵を多く
1. place-value-to-100 ✓
2. counting-in-2s-3s-5s-and-10s ✓
3. number-bonds-to-20-and-100 ✓
4. adding-and-subtracting-2-digit-numbers ✓
5. 2-5-and-10-times-tables ✓
6. multiplication-and-division ✓
7. fractions ✓
8. money ✓
9. telling-the-time-to-5-minutes ✓
10. measuring ✓
11. 2d-and-3d-shapes ✓
12. position-and-direction ✓
13. pictograms-and-tally-charts ✓

UK / Maths / Year 1（KS1）— 100 まで（計算は 20 まで）。とても短い文、ほぼ全問に絵
1. counting-to-100 ✓
2. number-bonds-to-10-and-20 ✓
3. addition-and-subtraction-within-20 ✓
4. counting-in-2s-5s-and-10s ✓
5. halves-and-quarters ✓
6. length-height-mass-and-capacity ✓
7. money ✓
8. time ✓
9. 2d-and-3d-shapes ✓
10. position-and-direction ✓

AU / Maths（Australian Curriculum v9.0）— country `au`、subject `maths`、grade `year-N`、A4。
オーストラリア英語（colour, metre, maths, analog, mixed numeral, column graph, students）。お金は $ と c（1c・2c 硬貨なし）。
数は 4 桁はそのまま（4536）、5 桁以上は空白区切り（10 000、ノーブレークスペース）。standard_code は v9 のコード（例: AC9M3N01）

AU / Maths / Year 3（NAPLAN の学年）
1. place-value-to-10000 ✓
2. adding-and-subtracting ✓
3. mental-strategies-and-number-sentences ✓
4. multiplication-facts-3-4-5-and-10 ✓
5. multiplying-and-dividing ✓
6. fractions ✓
7. money ✓
8. measuring-length-mass-and-capacity ✓
9. telling-the-time ✓
10. angles-as-turns ✓
11. 3d-objects ✓
12. maps-and-locations ✓
13. data-and-graphs ✓
14. chance ✓

AU / Maths / Year 5（NAPLAN の学年）
1. decimals ✓
2. factors-and-multiples ✓
3. comparing-fractions ✓
4. percentages ✓
5. adding-and-subtracting-fractions ✓
6. multiplication ✓
7. division ✓
8. estimation-and-money-problems ✓
9. number-sentences-multiplication-and-division ✓
10. metric-units ✓
11. perimeter-and-area ✓
12. 12-and-24-hour-time ✓
13. measuring-angles ✓
14. nets ✓
15. coordinates-and-transformations ✓
16. line-graphs-and-data ✓
17. chance ✓

AU / Maths / Year 4
1. multiplication-facts-to-10-x-10 ✓
2. decimals-tenths-and-hundredths ✓
3. equivalent-fractions ✓
4. multiplication-and-division-strategies ✓
5. adding-and-subtracting-large-numbers ✓
6. multiplying-and-dividing-by-10-and-100 ✓
7. counting-by-fractions-and-mixed-numerals ✓
8. rounding-and-estimation ✓
9. money-and-financial-problems ✓
10. odd-and-even-numbers ✓
11. number-sentences-addition-and-subtraction ✓
12. reading-scales-and-temperature ✓
13. perimeter-and-area ✓
14. time-am-pm-and-duration ✓
15. comparing-angles ✓
16. grid-references-and-maps ✓
17. symmetry ✓
18. shapes-and-composite-objects ✓
19. data-and-graphs ✓
20. chance ✓

AU / Maths / Year 6（高校準備の学年。NAPLAN はない）
1. integers-and-negative-numbers ✓
2. prime-composite-and-square-numbers ✓
3. comparing-and-ordering-fractions ✓
4. adding-and-subtracting-fractions ✓
5. adding-and-subtracting-decimals ✓
6. multiplying-and-dividing-decimals-by-powers-of-10 ✓
7. percentages-of-quantities ✓
8. estimation-and-financial-problems ✓
9. multiplying-and-dividing-larger-numbers ✓
10. number-patterns ✓
11. order-of-operations-and-equations ✓
12. converting-metric-units ✓
13. area-of-rectangles ✓
14. timetables-and-itineraries ✓
15. angles-on-a-line-and-at-a-point ✓
16. prisms-and-cross-sections ✓
17. cartesian-plane-four-quadrants ✓
18. transformations-and-tessellations ✓
19. interpreting-data ✓
20. probability ✓

AU / Maths / Year 2（文は短く、絵を多く。NAPLAN はない）
1. place-value-to-1000 ✓
2. addition-and-subtraction-facts-to-20 ✓
3. adding-and-subtracting-2-digit-numbers ✓
4. word-problems-and-number-sentences ✓
5. twos-doubling-and-halving ✓
6. multiplying-and-dividing-with-groups ✓
7. money ✓
8. halves-quarters-and-eighths ✓
9. number-patterns ✓
10. telling-the-time-to-the-quarter-hour ✓
11. calendars-and-dates ✓
12. measuring-length-mass-and-capacity ✓
13. turns ✓
14. 2d-shapes ✓
15. maps-and-directions ✓
16. data-tables-and-graphs ✓

AU / Maths / Year 1（とても短い文、ほぼ全問に絵）
1. numbers-to-120 ✓
2. tens-and-ones ✓
3. addition-and-subtraction-within-20 ✓
4. skip-counting-by-2s-5s-and-10s ✓
5. word-problems-and-money ✓
6. sharing-and-grouping ✓
7. repeating-patterns ✓
8. measuring-and-comparing ✓
9. days-weeks-months-and-time ✓
10. shapes-and-objects ✓
11. position-and-directions ✓
12. data-and-tally-marks ✓
13. chance ✓

CA-ON / Math（Ontario Curriculum 2020）— country `ca-on`（name「Ontario, Canada」）、subject `math`、grade `grade-N`、Letter。生成スクリプトは `gen_caon_math_*`。
カナダ英語（colour, metre, centre, math, grade, students, trapezoid, counterclockwise, bar graph）。お金は $ と ¢（nickel 5¢・dime・quarter・loonie・toonie、ペニーなし）。
数は 4 桁はそのまま、5 桁以上はノーブレークスペース区切り。standard_code は「Grade 3: B2.2」形式。EQAO は Grade 3・6

CA-ON / Math / Grade 3（EQAO の学年）
1. multiplication-facts-for-2-5-and-10 ✓
2. numbers-to-1000 ✓
3. adding-and-subtracting-to-1000 ✓
4. multiplication-and-division ✓
5. fractions-and-fair-shares ✓
6. rounding-and-estimating ✓
7. patterns ✓
8. equations-and-equivalence ✓
9. money-and-making-change ✓
10. telling-time ✓
11. length-and-perimeter ✓
12. mass-and-capacity ✓
13. area ✓
14. 2d-shapes-and-3d-objects ✓
15. location-and-movement ✓
16. data-and-graphs ✓
17. probability ✓

CA-ON / Math / Grade 6（EQAO の学年）
1. fractions-decimals-and-percents ✓
2. integers ✓
3. large-numbers-and-decimals ✓
4. adding-and-subtracting-fractions ✓
5. adding-and-subtracting-decimals ✓
6. multiplying-and-dividing-decimals ✓
7. multiplying-and-dividing-with-fractions ✓
8. factors-primes-and-divisibility ✓
9. ratios-rates-and-percents ✓
10. patterns-and-expressions ✓
11. equations-and-inequalities ✓
12. area-of-polygons ✓
13. measuring-angles ✓
14. cartesian-plane-and-transformations ✓
15. quadrilaterals-and-congruence ✓
16. metric-units-and-time ✓
17. data-and-graphs ✓
18. probability ✓
19. financial-literacy ✓

CA-ON / Math / Grade 4（EQAO なし）
1. multiplication-facts-to-10-x-10 ✓
2. numbers-to-10000 ✓
3. rounding-and-estimating ✓
4. adding-and-subtracting-to-10000 ✓
5. multiplying-by-one-digit-numbers ✓
6. dividing-by-one-digit-numbers ✓
7. fractions ✓
8. decimal-tenths ✓
9. patterns ✓
10. equations-and-inequalities ✓
11. data-and-graphs ✓
12. probability ✓
13. angles-and-rectangles ✓
14. coordinates-and-transformations ✓
15. mass-capacity-and-metric-units ✓
16. elapsed-time ✓
17. area-of-rectangles ✓
18. money-and-financial-literacy ✓

CA-ON / Math / Grade 5（EQAO なし。HST 13% は financial-literacy のみ）
1. multiplication-facts-to-12-x-12 ✓
2. numbers-to-100000 ✓
3. adding-and-subtracting-whole-numbers-and-decimals ✓
4. multiplying-two-digit-numbers ✓
5. dividing-by-two-digit-numbers ✓
6. equivalent-fractions-and-mixed-numbers ✓
7. decimals-to-hundredths ✓
8. fractions-decimals-and-percents ✓
9. multiplying-and-dividing-with-unit-fractions ✓
10. ratios-and-rates ✓
11. patterns ✓
12. expressions-equations-and-inequalities ✓
13. data-and-graphs ✓
14. probability ✓
15. triangles-and-congruence ✓
16. coordinates-and-transformations ✓
17. measuring-angles ✓
18. area-of-parallelograms-and-triangles ✓
19. metric-conversions ✓
20. financial-literacy ✓

CA-ON / Math / Grade 2（200 まで。文は短く、絵を多く）
1. numbers-to-200 ✓
2. counting-to-200 ✓
3. odd-and-even-numbers ✓
4. addition-and-subtraction-facts-to-20 ✓
5. adding-and-subtracting-to-100 ✓
6. equal-groups-and-sharing ✓
7. fractions-and-fair-shares ✓
8. patterns ✓
9. equality-and-missing-numbers ✓
10. data-and-graphs ✓
11. probability ✓
12. 2d-shapes-and-symmetry ✓
13. maps-and-directions ✓
14. measuring-length ✓
15. time ✓
16. money ✓

CA-ON / Math / Grade 1（50 まで。とても短い文、ほぼ全問に絵）
1. numbers-to-50 ✓
2. counting-and-estimating-to-50 ✓
3. addition-and-subtraction-facts-to-10 ✓
4. adding-and-subtracting-to-20 ✓
5. word-problems-to-50 ✓
6. equal-groups-and-fair-shares ✓
7. patterns ✓
8. equal-and-not-equal ✓
9. sorting-and-graphs ✓
10. probability ✓
11. 2d-shapes-and-3d-objects ✓
12. position-and-directions ✓
13. comparing-length-mass-and-capacity ✓
14. calendar-days-weeks-and-months ✓
15. money ✓

CA-ON / Math / Grade 7（EQAO なし。10億まで、負の数は −）
1. powers-and-large-numbers ✓
2. perfect-squares-and-square-roots ✓
3. comparing-fractions-and-decimals ✓
4. fractions-decimals-and-percents ✓
5. adding-and-subtracting-integers ✓
6. adding-and-subtracting-fractions ✓
7. gcf-and-lcm ✓
8. multiplying-and-dividing-fractions ✓
9. multiplying-and-dividing-decimals ✓
10. proportional-reasoning ✓
11. order-of-operations ✓
12. linear-growing-patterns ✓
13. algebraic-expressions ✓
14. equations-and-inequalities ✓
15. circle-graphs-and-data ✓
16. probability-of-independent-and-dependent-events ✓
17. transformations-and-dilations ✓
18. circles ✓
19. surface-area-and-volume ✓
20. exchange-rates-and-interest ✓

CA-ON / Math / Grade 8（EQAO なし。次は Grade 9）
1. scientific-notation ✓
2. square-roots-and-real-numbers ✓
3. percents ✓
4. adding-and-subtracting-integers ✓
5. multiplying-and-dividing-integers ✓
6. operations-with-fractions ✓
7. order-of-operations-with-rational-numbers ✓
8. proportional-relationships ✓
9. linear-relations ✓
10. expressions-and-binomials ✓
11. equations-and-inequalities ✓
12. scatter-plots-and-data ✓
13. probability-venn-and-tree-diagrams ✓
14. tessellations-and-transformations ✓
15. scale-drawings ✓
16. angle-properties ✓
17. pythagorean-theorem ✓
18. composite-area-and-volume ✓
19. interest-and-credit ✓

CA-BC / Math（BC Mathematics Curriculum K–9）— country `ca-bc`（name「British Columbia, Canada」）、subject `math`、grade `grade-N`、Letter。生成スクリプトは `gen_cabc_math_*`。
Ontario と同じカナダ英語・お金・数の書き方。税は GST 5% + PST 7%（HST・13% は使わない）。評価は FSA（Grade 4・7）。
standard_code は「Grade 4: Number」形式、standard_text は BC の Content 原文、standard_url は https://curriculum.gov.bc.ca/curriculum/mathematics/N/core

CA-BC / Math / Grade 4（FSA の学年）
1. multiplication-and-division-facts-to-100 ✓
2. numbers-to-10000 ✓
3. adding-and-subtracting-to-10000 ✓
4. multiplying-and-dividing-by-one-digit-numbers ✓
5. comparing-and-ordering-fractions ✓
6. decimals-to-hundredths ✓
7. adding-and-subtracting-decimals ✓
8. one-step-equations ✓
9. increasing-and-decreasing-patterns ✓
10. 12-and-24-hour-time ✓
11. regular-and-irregular-polygons ✓
12. perimeter ✓
13. line-symmetry ✓
14. bar-graphs-and-pictographs ✓
15. probability-experiments ✓
16. money-and-making-change ✓

CA-BC / Math / Grade 7（FSA の学年）
1. adding-and-subtracting-integers ✓
2. multiplying-and-dividing-integers ✓
3. order-of-operations ✓
4. adding-and-subtracting-decimals ✓
5. multiplying-and-dividing-decimals ✓
6. fractions-decimals-and-percents ✓
7. ratios ✓
8. two-step-equations ✓
9. linear-relations ✓
10. circumference-and-area-of-circles ✓
11. volume-of-prisms-and-cylinders ✓
12. cartesian-coordinates-and-graphing ✓
13. combinations-of-transformations ✓
14. circle-graphs ✓
15. probability-of-two-independent-events ✓
16. financial-percentages ✓

CA-BC / Math / Grade 1（文はとても短く、絵を多く）
1. numbers-to-20 ✓
2. ways-to-make-10 ✓
3. addition-and-subtraction-to-20 ✓
4. change-in-quantity ✓
5. equal-and-not-equal ✓
6. repeating-patterns ✓
7. measuring-with-non-standard-units ✓
8. 2d-shapes-and-3d-objects ✓
9. concrete-graphs ✓
10. likelihood ✓
11. coins-and-money ✓

CA-BC / Math / Grade 2（文は短く、絵を多く）
1. numbers-to-100 ✓
2. benchmarks-25-50-and-100 ✓
3. addition-and-subtraction-facts-to-20 ✓
4. adding-and-subtracting-to-100 ✓
5. change-in-quantity ✓
6. equality-and-inequality ✓
7. repeating-and-increasing-patterns ✓
8. measuring-length ✓
9. 2d-shapes-and-3d-objects ✓
10. pictographs ✓
11. likelihood ✓
12. coins-to-100-cents ✓

CA-BC / Math / Grade 3
1. numbers-to-1000 ✓
2. fractions ✓
3. adding-and-subtracting-to-1000 ✓
4. multiplication-and-division ✓
5. one-step-equations ✓
6. increasing-and-decreasing-patterns ✓
7. measuring-length-mass-and-capacity ✓
8. time ✓
9. 3d-objects ✓
10. bar-graphs-and-pictographs ✓
11. likelihood-of-simulated-events ✓
12. money-to-100-dollars ✓

CA-BC / Math / Grade 5
1. numbers-to-1000000 ✓
2. decimals-to-thousandths ✓
3. equivalent-fractions ✓
4. benchmarks-and-estimation ✓
5. adding-and-subtracting-whole-numbers ✓
6. multiplication-to-three-digits ✓
7. division-with-remainders ✓
8. adding-and-subtracting-decimals ✓
9. one-step-equations-with-variables ✓
10. pattern-rules ✓
11. area-and-perimeter ✓
12. duration-of-time ✓
13. prisms-and-pyramids ✓
14. single-transformations ✓
15. double-bar-graphs ✓
16. probability-experiments ✓
17. money-and-financial-plans ✓

CA-BC / Math / Grade 6
1. thousandths-to-billions ✓
2. gcf-and-lcm ✓
3. improper-fractions-and-mixed-numbers ✓
4. ratios ✓
5. percents-and-discounts ✓
6. order-of-operations ✓
7. multiplying-and-dividing-decimals ✓
8. one-step-equations ✓
9. patterns-tables-and-graphs ✓
10. perimeter-of-complex-shapes ✓
11. area-of-triangles-parallelograms-and-trapezoids ✓
12. angles ✓
13. volume-and-capacity ✓
14. triangles ✓
15. combinations-of-transformations ✓
16. line-graphs ✓
17. probability ✓
18. budgeting-and-consumer-math ✓

CA-BC / Math / Grade 8
1. squares-cubes-and-roots ✓
2. percents-less-than-1-and-greater-than-100 ✓
3. proportional-reasoning ✓
4. adding-and-subtracting-fractions ✓
5. multiplying-and-dividing-fractions ✓
6. expressions-and-substitution ✓
7. two-step-equations ✓
8. linear-relations ✓
9. surface-area-and-volume ✓
10. pythagorean-theorem ✓
11. views-and-nets ✓
12. central-tendency ✓
13. probability-of-two-independent-events ✓
14. best-buys ✓

CA-BC / Math / Grade 9（Mathematics 9）
1. exponent-laws ✓
2. operations-with-rational-numbers ✓
3. adding-and-subtracting-polynomials ✓
4. multiplying-and-dividing-polynomials ✓
5. linear-equations ✓
6. linear-relations-and-graphs ✓
7. similar-shapes-and-scale-diagrams ✓
8. statistics-in-society ✓
9. budgets-and-transactions ✓

SG / Maths（MOE 2021 Primary Mathematics Syllabus, Standard）— country `sg`（name「Singapore」）、subject `maths`、grade `primary-N`（表示は「Primary N」/「PN」）、A4。生成スクリプトは `gen_sg_maths_pN_*`。
イギリス英語（colour, metre, maths, cuboid, trapezium, renaming, picture graph, multiplication tables）。単位は ℓ と ml、時刻は「7.30 am」（ドット・ピリオドなし）、24時間制は「1930」。お金は $ と ¢（5¢・10¢・20¢・50¢・$1 硬貨、1¢ は使わない）。GST 9% は P5 のみ。
数は 4 桁はそのまま、5 桁以上はノーブレークスペース区切り（MOE シラバスと同じ）。文章題は bar model（units）を使う。standard_code は「Primary 4: Fractions」形式、standard_url は https://www.moe.gov.sg/primary/curriculum/syllabus

SG / Maths / Primary 6（PSLE の学年。PSLE はここだけタイトルに入れる）
1. dividing-fractions ✓
2. fraction-word-problems ✓
3. percentage ✓
4. ratio ✓
5. ratio-word-problems ✓
6. algebra ✓
7. area-and-circumference-of-circles ✓
8. volume-of-cubes-and-cuboids ✓
9. angles-in-composite-figures ✓
10. average ✓

SG / Maths / Primary 5
1. numbers-to-10-million ✓
2. multiplying-and-dividing-by-10-100-1000 ✓
3. order-of-operations ✓
4. fractions-and-division ✓
5. adding-and-subtracting-mixed-numbers ✓
6. multiplying-fractions ✓
7. decimals-and-measurement ✓
8. percentage ✓
9. discount-gst-and-interest ✓
10. rate ✓
11. area-of-triangles ✓
12. volume-of-cubes-and-cuboids ✓
13. angles ✓
14. triangles ✓
15. parallelograms-rhombuses-and-trapeziums ✓

SG / Maths / Primary 4
1. numbers-to-100000 ✓
2. rounding-and-estimation ✓
3. factors-and-multiples ✓
4. multiplication ✓
5. division ✓
6. mixed-numbers-and-improper-fractions ✓
7. fraction-of-a-set ✓
8. adding-and-subtracting-fractions ✓
9. decimals ✓
10. adding-and-subtracting-decimals ✓
11. multiplying-and-dividing-decimals ✓
12. area-and-perimeter ✓
13. angles ✓
14. rectangles-and-squares ✓
15. line-symmetry ✓
16. nets ✓
17. tables-line-graphs-and-pie-charts ✓

SG / Maths / Primary 3
1. numbers-to-10000 ✓
2. addition-and-subtraction ✓
3. multiplication-tables-6-7-8-and-9 ✓
4. multiplication-and-division ✓
5. equivalent-fractions ✓
6. adding-and-subtracting-fractions ✓
7. money ✓
8. length-mass-and-volume ✓
9. time ✓
10. area-and-perimeter ✓
11. angles ✓
12. perpendicular-and-parallel-lines ✓
13. bar-graphs ✓

SG / Maths / Primary 2（文は短く、絵を多く）
1. numbers-to-1000 ✓
2. odd-and-even-numbers ✓
3. addition-and-subtraction ✓
4. multiplication-tables-2-3-4-5-and-10 ✓
5. multiplication-and-division ✓
6. fractions ✓
7. adding-and-subtracting-fractions ✓
8. money ✓
9. length-mass-and-volume ✓
10. time ✓
11. 2d-shapes-and-patterns ✓
12. 3d-shapes ✓
13. picture-graphs ✓

SG / Maths / Primary 1（とても短い文、ほぼ全問に絵）
1. numbers-to-100 ✓
2. ordinal-numbers ✓
3. number-bonds ✓
4. addition-and-subtraction-within-20 ✓
5. addition-and-subtraction-within-100 ✓
6. multiplication-and-division ✓
7. money ✓
8. length ✓
9. time ✓
10. 2d-shapes ✓
11. picture-graphs ✓
US / Math / Grade 7（Common Core）— 1,000 以上はカンマ付き。負の数は「−」（U+2212）。共通部品は `tools/ws_common.py`
1. adding-and-subtracting-integers ✓
2. multiplying-and-dividing-integers ✓
3. two-step-equations ✓
4. proportional-relationships ✓
5. percent-problems ✓
6. simplifying-expressions ✓
7. circles-area-and-circumference ✓
8. angle-relationships ✓
9. probability ✓
10. two-step-inequalities ✓
11. unit-rates-with-fractions
12. rational-number-word-problems
13. converting-fractions-to-decimals
14. scale-drawings
15. area-surface-area-volume
16. compound-probability
17. random-sampling
18. comparing-data-distributions
19. constructing-triangles-and-cross-sections

US / Math / Grade 8（Common Core）
1. linear-equations 2. systems-of-equations 3. slope 4. functions 5. linear-functions 6. exponent-rules
7. scientific-notation 8. square-and-cube-roots 9. rational-and-irrational-numbers 10. pythagorean-theorem
11. transformations 12. congruence-and-similarity 13. angle-relationships-parallel-lines
14. volume-of-cylinders-cones-spheres 15. scatter-plots 16. two-way-tables 17. distance-on-coordinate-plane

US / Math / Kindergarten（Common Core）— 次に作る

その後: UK Year 7–9（KS3）、AU Year 7–8、AU Foundation、SG Secondary 1–2、CA-BC Kindergarten、US Texas (TEKS) …（新しい学年・国は `catalog.json` に追加）

## 触ってはいけないもの

- `site/worksheets/inc/secret.php`（サーバーにだけある鍵。リポジトリに入れない）
- DB は ws_ で始まる4テーブル以外を変更しない（`api/sync.php` もこの4つしか書かない）
- `/aplus/` の他のフォルダ、`/aplus/sitemap.php`（このリポジトリの外）
