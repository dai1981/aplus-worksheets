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

新しい国は GDP の高い順（中国本土は Google が使えず AdSense の効果が小さいので後回し）

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

UK / Maths / Year 7–9（KS3。National Curriculum の KS3 は 3 学年まとめての内容なので、White Rose 等の一般的な配分で学年に分ける）— Year 4 と同じルール。
生成スクリプトは `gen_uk_maths_y7_*`、共通部品は `tools/uk_ks3.py`（ws_common の上に UK の名前・£・make）。負の数は「−」。standard_code は「KS3: Number」形式（Number／Algebra／Ratio, proportion and rates of change／Geometry and measures／Probability／Statistics）

UK / Maths / Year 7
1. place-value-and-ordering ✓ 2. negative-numbers ✓ 3. order-of-operations ✓ 4. factors-multiples-and-primes ✓ 5. powers-and-roots ✓
6. rounding-and-estimation ✓ 7. fractions-decimals-and-percentages ✓ 8. adding-and-subtracting-fractions ✓ 9. multiplying-and-dividing-fractions ✓
10. percentages-of-amounts ✓ 11. algebraic-notation-and-substitution ✓ 12. simplifying-expressions ✓ 13. solving-equations ✓ 14. sequences ✓
15. ratio-and-proportion ✓ 16. angles ✓ 17. perimeter-and-area ✓ 18. coordinates-and-straight-line-graphs ✓ 19. averages-and-range ✓ 20. probability ✓

UK / Maths / Year 8
1. indices ✓ 2. standard-form ✓ 3. expanding-and-factorising ✓ 4. equations-with-unknowns-on-both-sides ✓ 5. inequalities ✓
6. changing-the-subject-of-a-formula ✓ 7. linear-graphs ✓ 8. percentage-change-and-interest ✓ 9. direct-and-inverse-proportion ✓
10. speed-distance-and-time ✓ 11. circles ✓ 12. volume-and-surface-area-of-prisms ✓ 13. angles-in-parallel-lines-and-polygons ✓
14. transformations ✓ 15. probability-of-combined-events ✓ 16. frequency-tables-and-charts ✓ 17. units-and-scale-drawings ✓

UK / Maths / Year 9
1. pythagoras-theorem ✓ 2. trigonometry ✓ 3. similarity-and-congruence ✓ 4. expanding-and-factorising-quadratics ✓ 5. simultaneous-equations ✓
6. quadratic-graphs ✓ 7. arithmetic-and-geometric-sequences ✓ 8. compound-interest-and-growth ✓ 9. volume-of-cylinders-cones-and-spheres ✓
10. arcs-and-sectors ✓ 11. bearings-and-loci ✓ 12. scatter-graphs-and-correlation ✓ 13. plans-and-elevations ✓ 14. real-life-graphs ✓
15. rounding-and-error-intervals ✓ 16. ratio-problems-and-best-buys ✓

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

AU / Maths / Foundation（最初の学年。州ごとに Kindergarten・Prep・Pre-primary・Reception・Transition と呼ぶ。5〜6歳）— grade `foundation`（name「Foundation」、sort 0）。生成スクリプトは `gen_au_maths_f_*`、共通部品は `tools/f_common.py`（k_pics・k_common の上にオーストラリア英語・AU の名前・sky_svg・days_svg・pictograph_svg・pattern_svg・glasses_svg・make）。とても短い文、ほぼ全問に絵。unit.php で educationalLevel に州ごとの呼び名を入れる
1. numbers-to-20 ✓ 2. subitising-to-5 ✓ 3. counting-and-comparing-collections ✓ 4. part-part-whole-to-10 ✓ 5. adding-and-taking-away ✓ 6. sharing-and-grouping ✓
7. repeating-patterns ✓ 8. comparing-length-mass-and-capacity ✓ 9. days-and-times-of-day ✓ 10. shapes ✓ 11. position-and-location ✓ 12. sorting-and-data ✓

AU / Maths / Year 7–8（高校。生成スクリプトは `gen_au_maths_y7_*`・`gen_au_maths_y8_*`、共通部品は `tools/au_hs.py`（ws_common の上に AU の数の書き方・$・make）。負の数は「−」。standard_code は v9 のコード（例: AC9M8N04）、standard_url は v9 の Mathematics ページ）

AU / Maths / Year 7
1. square-numbers-and-square-roots ✓ 2. prime-factorisation-and-index-notation ✓ 3. fractions-decimals-and-percentages ✓ 4. rounding-and-estimation ✓ 5. adding-and-subtracting-fractions ✓ 6. multiplying-and-dividing-fractions ✓
7. percentages-and-discounts ✓ 8. adding-and-subtracting-integers ✓ 9. ratios ✓ 10. formulas-and-substitution ✓ 11. algebraic-expressions ✓ 12. solving-linear-equations ✓
13. area-of-triangles-and-parallelograms ✓ 14. volume-of-prisms ✓ 15. circumference-and-pi ✓ 16. angles-and-parallel-lines ✓ 17. angle-sum-of-triangles-and-polygons ✓ 18. transformations-on-the-cartesian-plane ✓
19. mean-median-mode-and-range ✓ 20. stem-and-leaf-plots ✓ 21. probability ✓

AU / Maths / Year 8
1. irrational-numbers-and-recurring-decimals ✓ 2. index-laws ✓ 3. integers-and-rational-numbers ✓ 4. percentages-profit-and-loss ✓ 5. expanding-and-factorising ✓ 6. linear-equations ✓
7. linear-inequalities ✓ 8. graphing-linear-relations ✓ 9. area-and-perimeter-of-composite-shapes ✓ 10. volume-and-capacity ✓ 11. circumference-and-area-of-circles ✓ 12. time-zones-and-duration ✓
13. rates ✓ 14. pythagoras-theorem ✓ 15. congruent-and-similar-triangles ✓ 16. properties-of-quadrilaterals ✓ 17. sampling-and-data ✓ 18. probability-of-two-events ✓

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

CA-BC / Math / Kindergarten（5〜6歳）— grade `kindergarten`（name「Kindergarten」、sort 0）。10 まで。とても短い文、ほぼ全問に絵。生成スクリプトは `gen_cabc_math_k_*`、共通部品は `tools/bck_common.py`（k_pics・k_common の上にカナダ英語・BC の名前・mcq（10 を超える誤答を落とす）・collect・letters・finish・make）。AU Foundation と BC Grade 1 の問題関数・絵を再利用。standard_code は「Kindergarten: Number」形式
1. numbers-to-10 ✓ 2. ways-to-make-5 ✓ 3. comparing-quantities-to-10 ✓ 4. decomposing-numbers-to-10 ✓ 5. change-in-quantity-to-10 ✓ 6. repeating-patterns ✓
7. equal-and-not-equal ✓ 8. comparing-length-mass-and-capacity ✓ 9. 2d-shapes-and-3d-objects ✓ 10. concrete-graphs ✓ 11. likelihood ✓ 12. canadian-coins ✓

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

SG / Maths / Secondary 1–4（MOE 2020 O-Level / G3 Mathematics。旧 Express）— grade `secondary-N`（表示は「Secondary N」、sort 7〜10、12〜16歳。Sec 4 が O-Level の学年）。生成スクリプトは `gen_sg_maths_sN_*`、共通部品は `tools/sg_sec.py`（uk_ks3 と同じ API。SG の名前・$・数の書き方、STD_TEXT（シラバス原文）、TITLES、seo_title は make が自動。`adopt(mod, R)` で他国の生成スクリプトの問題関数を SG の名前・$・数の書き方のまま再利用できる）。Sec 3–4 は答えを 3 有効数字・角度は小数第 1 位（O-Level と同じ）。
多くは UK KS3 の生成スクリプトを SG 式に移したもの（£→$、miles→km、VAT→GST 9%、stem-and-leaf diagram）。負の数は「−」。standard_code は「Secondary 1: Ratio and Proportion」形式（N1〜N7・G1〜G5・S1〜S2 の小項目名）、standard_url は MOE 2020 Express/N(A) シラバス PDF

SG / Maths / Secondary 1
1. primes-hcf-and-lcm ✓ 2. integers-and-the-number-line ✓ 3. approximation-and-estimation ✓ 4. ratio ✓ 5. percentage ✓ 6. rate-and-speed ✓
7. algebraic-expressions-and-substitution ✓ 8. simplifying-linear-expressions ✓ 9. number-patterns ✓ 10. linear-equations ✓ 11. linear-graphs-and-gradient ✓
12. angles-triangles-and-quadrilaterals ✓ 13. parallel-lines-and-polygons ✓ 14. perimeter-and-area ✓ 15. volume-and-surface-area-of-prisms-and-cylinders ✓

SG / Maths / Secondary 2
1. expansion-and-factorisation ✓ 2. algebraic-fractions ✓ 3. changing-the-subject-of-a-formula ✓ 4. linear-inequalities ✓ 5. simultaneous-equations ✓
6. quadratic-equations ✓ 7. quadratic-graphs ✓ 8. direct-and-inverse-proportion ✓ 9. map-scales ✓ 10. congruence-and-similarity ✓ 11. pythagoras-theorem ✓
12. trigonometric-ratios ✓ 13. volume-of-cones-and-spheres ✓ 14. mean-median-and-mode ✓ 15. stem-and-leaf-diagrams ✓ 16. frequency-tables-and-grouped-data ✓ 17. probability ✓

SG / Maths / Secondary 3
1. indices ✓ 2. standard-form ✓ 3. quadratic-formula-and-completing-the-square ✓ 4. fractional-equations ✓ 5. quadratic-equation-word-problems ✓
6. simultaneous-linear-inequalities ✓ 7. sketching-quadratic-graphs ✓ 8. power-and-exponential-graphs ✓ 9. coordinate-geometry ✓ 10. congruent-and-similar-triangles ✓
11. area-and-volume-of-similar-figures ✓ 12. sine-and-cosine-rules ✓ 13. bearings-and-angles-of-elevation ✓ 14. arc-length-sector-area-and-radians ✓
15. symmetry-properties-of-circles ✓ 16. angle-properties-of-circles ✓

SG / Maths / Secondary 4（O-Level の学年）
1. sets-and-venn-diagrams ✓ 2. matrices ✓ 3. vectors ✓ 4. vector-geometry ✓ 5. problems-in-three-dimensions ✓
6. cumulative-frequency-and-box-plots ✓ 7. standard-deviation ✓ 8. probability-of-combined-events ✓

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
11. unit-rates-with-fractions ✓
12. rational-number-word-problems ✓
13. converting-fractions-to-decimals ✓
14. scale-drawings ✓
15. area-surface-area-volume ✓
16. compound-probability ✓
17. random-sampling ✓
18. comparing-data-distributions ✓
19. constructing-triangles-and-cross-sections ✓

US / Math / Grade 8（Common Core）— 1,000 以上はカンマ付き。負の数は「−」。生成スクリプトは `gen_us_math_g8_*`（共通部品は `tools/ws_common.py`）
1. linear-equations ✓
2. systems-of-equations ✓
3. slope ✓
4. functions ✓
5. linear-functions ✓
6. exponent-rules ✓
7. scientific-notation ✓
8. square-and-cube-roots ✓
9. rational-and-irrational-numbers ✓
10. pythagorean-theorem ✓
11. transformations ✓
12. congruence-and-similarity ✓
13. angle-relationships-parallel-lines ✓
14. volume-of-cylinders-cones-spheres ✓
15. scatter-plots ✓
16. two-way-tables ✓
17. distance-on-coordinate-plane ✓

US / Math / Kindergarten（Common Core）— grade `kindergarten`（name「Kindergarten」、sort 0、5〜6歳）。生成スクリプトは `gen_us_math_gk_*`、絵の部品は `tools/k_pics.py`。
20 まで（数えるのは 100 まで）。文はとても短く、5〜6歳が読める英語で。ほぼ全問に絵。standard_code は「K.CC.B.5」形式
1. counting-to-20 ✓
2. counting-to-100 ✓
3. writing-numbers-0-to-20 ✓
4. comparing-numbers ✓
5. addition-within-10 ✓
6. subtraction-within-10 ✓
7. make-10 ✓
8. decompose-numbers-to-10 ✓
9. add-and-subtract-within-5 ✓
10. teen-numbers-tens-and-ones ✓
11. compare-length-and-weight ✓
12. sort-and-count ✓
13. 2d-and-3d-shapes ✓
14. positions ✓
15. build-and-compose-shapes ✓

US / Math / Algebra 1（Common Core 高校）— grade `algebra-1`（name「Algebra 1」、sort 9、14〜15歳）。1,000 以上はカンマ付き。負の数は「−」。生成スクリプトは `gen_us_math_a1_*`、共通部品は `tools/us_hs.py`（au_hs と同じ API。make は CCSS の高校コード「A-REI.B.3」から standard_url を作る。domain は引数で指定）。トピック `quadratics` あり
1. multi-step-equations ✓ 2. literal-equations ✓ 3. multi-step-and-compound-inequalities ✓ 4. absolute-value-equations-and-inequalities ✓ 5. function-notation ✓
6. domain-and-range ✓ 7. forms-of-linear-equations ✓ 8. systems-of-linear-equations ✓ 9. systems-of-linear-inequalities ✓ 10. rational-exponents ✓
11. simplifying-radicals ✓ 12. exponential-growth-and-decay ✓ 13. arithmetic-and-geometric-sequences ✓ 14. polynomial-operations ✓ 15. factoring-polynomials ✓
16. solving-quadratics-by-factoring ✓ 17. quadratic-formula-and-completing-the-square ✓ 18. graphing-quadratic-functions ✓ 19. box-plots-and-standard-deviation ✓ 20. correlation-and-residuals ✓

US / Math / Geometry（Common Core 高校）— grade `geometry`（name「Geometry」、sort 10、15〜16歳）。生成スクリプトは `gen_us_math_ge_*`、共通部品は `tools/us_hs.py`（make に grade="geometry"）と図の部品 `tools/us_geo.py`（Canvas: poly・angle・right・ticks・chevrons・side_label など）。domain は引数で指定。トピック `circles`・`congruence-and-similarity` あり
1. points-lines-and-planes ✓ 2. segment-addition-and-midpoints ✓ 3. distance-and-midpoint-formulas ✓ 4. angle-pairs ✓ 5. conditional-statements-and-proof ✓
6. parallel-lines-and-transversals ✓ 7. slopes-of-parallel-and-perpendicular-lines ✓ 8. rigid-transformations ✓ 9. triangle-angle-theorems ✓ 10. congruent-triangles ✓
11. midsegments-and-triangle-centers ✓ 12. polygons-and-quadrilaterals ✓ 13. dilations-and-similarity ✓ 14. similar-triangles ✓ 15. pythagorean-theorem-and-special-right-triangles ✓
16. right-triangle-trigonometry ✓ 17. law-of-sines-and-cosines ✓ 18. circle-angles-and-arcs ✓ 19. arc-length-and-sector-area ✓ 20. equations-of-circles ✓
21. volume-of-solids ✓ 22. cross-sections-and-solids-of-revolution ✓ 23. conditional-probability ✓

US / Math / Algebra 2（Common Core 高校）— grade `algebra-2`（name「Algebra 2」、sort 11、16〜17歳）。生成スクリプトは `gen_us_math_a2_*`、共通部品は `tools/us_hs.py`（make に grade="algebra-2"）と多項式の部品 `tools/a2_common.py`（poly・pmul・peval・synth・sf・ps・lin）。domain は引数で指定。トピック `trigonometry` あり
1. complex-numbers ✓ 2. polynomial-division-and-remainder-theorem ✓ 3. polynomial-functions-and-zeros ✓ 4. polynomial-identities-and-factoring ✓ 5. rational-expressions ✓
6. rational-and-radical-equations ✓ 7. composition-and-inverse-functions ✓ 8. transformations-of-functions ✓ 9. exponential-functions-and-e ✓ 10. logarithms-and-their-properties ✓
11. exponential-and-logarithmic-equations ✓ 12. sequences-and-series ✓ 13. unit-circle-and-radians ✓ 14. graphs-of-sine-and-cosine ✓ 15. normal-distribution ✓
16. statistical-studies-and-margin-of-error ✓

US / Math / Precalculus（Common Core 高校の (+) 基準）— grade `precalculus`（name「Precalculus」、sort 12、17〜18歳）。生成スクリプトは `gen_us_math_pc_*`、共通部品は `tools/us_hs.py`（make に grade）と `tools/pc_common.py`（pis・trig・vhtml・surd・mat・det_h・vec・curve_svg など）。行列は `<span class='mx m2'>`（ws.css・ws-print.css）。トピック `vectors-and-matrices` あり
1. rational-functions-and-asymptotes ✓ 2. six-trigonometric-functions ✓ 3. inverse-trigonometric-functions ✓ 4. trigonometric-identities ✓ 5. sum-and-difference-formulas ✓
6. solving-trigonometric-equations ✓ 7. complex-numbers-in-polar-form ✓ 8. vectors ✓ 9. vector-operations ✓ 10. matrix-operations ✓
11. determinants-and-inverse-matrices ✓ 12. binomial-theorem ✓ 13. conic-sections ✓ 14. permutations-and-combinations ✓ 15. expected-value ✓
16. polar-coordinates ✓

TW / Math（十二年國教課綱・108課綱）— country `tw`（name「台灣」、lang `zh-TW`）、subject `math`（數學）、grade `grade-N`（國小N年級）、A4。生成スクリプトは `gen_tw_math_gN_*`、共通部品は `tools/tw_common.py`（num・mcq・lesson・make_unit・clock など）。
繁體中文・台灣用語（公分、毫米、公升、毫升、公斤、公克、元、直式、餘數、驗算）。時刻は「上午 9 時 40 分」、時間量は「1 小時 45 分鐘」。4 桁まではそのまま、10,000 以上はカンマ。餘數は「29 ÷ 4 ＝ 7……1」。
standard_code は課綱の學習內容コード（例: N-3-1）、standard_text は課綱の原文。domain は 數與量／空間與形狀／關係／資料與不確定性。body_html は「怎麼想 → 例題 → 常見錯誤」。
UI 文言は core.php の 'zh-TW'。プレビュー画像は Noto Sans TC のサブセットを使うので、**tw の単元を足したら `python3 tools/build_cjk_font.py` を実行してフォントもコミット**する（使う文字だけを入れる）。

TW / Math / Grade 3（國小三年級）
1. numbers-to-10000 ✓ 2. add-subtract-within-10000 ✓ 3. multiply-by-one-digit ✓ 4. division ✓ 5. divide-by-one-digit ✓
6. two-step-word-problems ✓ 7. estimation ✓ 8. fractions ✓ 9. decimals ✓ 10. number-line ✓ 11. millimeters ✓
12. angles ✓ 13. area-square-centimeters ✓ 14. liters-and-milliliters ✓ 15. kilograms-and-grams ✓ 16. time ✓
17. squares-and-rectangles ✓ 18. circles ✓ 19. nets ✓ 20. tables ✓ 21. multiplication-division-relationship ✓ 22. patterns ✓

TW / Math / Grade 4（國小四年級）
1. numbers-to-100-million ✓ 2. multi-digit-multiplication ✓ 3. multi-digit-division ✓ 4. two-step-word-problems ✓ 5. rounding ✓
6. fractions ✓ 7. equivalent-fractions ✓ 8. decimals ✓ 9. number-line ✓ 10. kilometers ✓ 11. angles ✓ 12. rotation ✓
13. area-and-perimeter ✓ 14. volume ✓ 15. time ✓ 16. perpendicular-and-parallel ✓ 17. congruent-figures ✓ 18. triangles ✓
19. quadrilaterals ✓ 20. order-of-operations ✓ 21. calculation-rules ✓ 22. formulas ✓ 23. patterns-odd-and-even ✓ 24. bar-and-line-graphs ✓

TW / Math / Grade 5（國小五年級）
1. place-value ✓ 2. multi-step-word-problems ✓ 3. factors-and-multiples ✓ 4. simplifying-fractions ✓ 5. adding-and-subtracting-fractions ✓
6. multiplying-fractions ✓ 7. fractions-as-division ✓ 8. dividing-fractions ✓ 9. multiplying-decimals ✓ 10. dividing-decimals ✓ 11. percentages ✓
12. rounding-decimals ✓ 13. area-units ✓ 14. metric-tons ✓ 15. volume-and-capacity ✓ 16. time-calculations ✓
17. triangle-and-quadrilateral-properties ✓ 18. area-of-triangles-and-quadrilaterals ✓ 19. sectors ✓ 20. line-symmetry ✓
21. volume-and-surface-area ✓ 22. faces-parallel-and-perpendicular ✓ 23. solids ✓ 24. three-step-problems-and-averages ✓
25. distributive-property ✓ 26. formulas-with-symbols ✓ 27. making-line-graphs ✓

TW / Math / Grade 6（國小六年級）— 圓周率は 3.14
1. prime-factorization ✓ 2. gcf-and-lcm ✓ 3. dividing-fractions ✓ 4. dividing-decimals ✓ 5. word-problems ✓ 6. ratios ✓
7. speed ✓ 8. base-and-compared-quantities ✓ 9. enlargement-and-reduction ✓ 10. map-scales ✓ 11. circumference ✓
12. area-of-circles ✓ 13. volume-of-prisms-and-cylinders ✓ 14. calculation-rules ✓ 15. quantity-relationships ✓
16. classic-word-problems ✓ 17. counting ✓ 18. pie-charts ✓ 19. likelihood ✓

TW / Math / Grade 7（國中七年級）— 負數は「－」（全角）、負數は（－5）とかっこ、式の部品は `tools/tw_g7.py`（sn・par・opv・lin・tidy_sets）
1. positive-and-negative-numbers ✓ 2. number-line-and-absolute-value ✓ 3. adding-and-subtracting-integers ✓
4. multiplying-and-dividing-integers ✓ 5. mixed-operations ✓ 6. laws-of-operations ✓ 7. exponents ✓ 8. scientific-notation ✓
9. primes ✓ 10. standard-factorization ✓ 11. algebraic-expressions ✓ 12. solving-linear-equations ✓ 13. equation-word-problems ✓
14. exponent-laws ✓ 15. systems-of-equations ✓ 16. solving-systems ✓ 17. coordinate-plane ✓ 18. graphs-of-linear-equations ✓
19. ratio-and-proportion ✓ 20. direct-and-inverse-proportion ✓ 21. linear-inequalities ✓ 22. geometry-symbols-and-perpendicular ✓
23. three-views ✓ 24. line-symmetry ✓ 25. statistical-charts ✓ 26. mean-median-mode ✓

TW / Math / Grade 8（國中八年級）— 根式は `tools/tw_g8.py`（poly・pmul・rt・simp・qroots）、線分は `<span class='ov'>AB</span>`
1. multiplication-formulas ✓ 2. polynomials ✓ 3. polynomial-multiplication-and-division ✓ 4. square-roots ✓ 5. operations-with-radicals ✓
6. approximating-square-roots ✓ 7. pythagorean-theorem ✓ 8. distance-formula ✓ 9. factoring ✓ 10. cross-method ✓ 11. quadratic-equations ✓
12. quadratic-formula ✓ 13. cumulative-relative-frequency ✓ 14. arithmetic-sequences ✓ 15. arithmetic-series ✓ 16. geometric-sequences ✓
17. linear-functions ✓ 18. parallel-lines ✓ 19. polygon-angle-sums ✓ 20. congruent-triangles ✓ 21. triangle-properties ✓
22. equilateral-triangle-area ✓ 23. parallelograms ✓ 24. special-quadrilaterals ✓

TW / Math / Grade 9（國中九年級）— 図の部品は `tools/tw_g9.py`（poly_svg・pi・vform・parab）。四分位數は前半・後半の中位數（資料の個數は 4 で割って 1 余る數を避ける）
1. continued-ratios ✓ 2. similar-figures ✓ 3. similar-triangles ✓ 4. proportional-segments ✓ 5. special-right-triangles ✓
6. arc-length-and-sector-area ✓ 7. points-lines-and-circles ✓ 8. inscribed-angles ✓ 9. circumcenter ✓ 10. incenter ✓ 11. centroid ✓
12. quadratic-functions ✓ 13. graphs-of-quadratic-functions ✓ 14. maximum-and-minimum ✓ 15. box-plots ✓ 16. probability ✓
17. lines-and-planes-in-space ✓ 18. surface-area-and-volume ✓ 19. geometric-proofs ✓

TW / Math / Grade 1（國小一年級）— 絵は `tools/tw_pics.py`（k_pics の絵に中國語の aria-label、台灣の硬幣・紙鈔 money_svg）。とても短い文、ほぼ全問に絵
1. numbers-to-100 ✓ 2. addition-meaning ✓ 3. subtraction-meaning ✓ 4. addition-facts-to-18 ✓ 5. subtraction-facts-to-18 ✓
6. add-subtract-within-100 ✓ 7. number-sentences ✓ 8. money ✓ 9. comparing-length ✓ 10. dates-and-time ✓ 11. shapes ✓
12. sorting-and-counting ✓

TW / Math / Grade 2（國小二年級）— 直式・積木・尺・分數の絵は `tools/tw_pics.py`（col・blocks・ruler・frac・array）。短い文、絵を多く
1. numbers-to-1000 ✓ 2. column-addition ✓ 3. column-subtraction ✓ 4. addition-subtraction-word-problems ✓ 5. estimation ✓ 6. money ✓
7. meaning-of-multiplication ✓ 8. multiplication-tables ✓ 9. sharing-and-grouping ✓ 10. two-step-problems ✓ 11. unit-fractions ✓
12. centimeters-and-meters ✓ 13. capacity-weight-and-area ✓ 14. telling-time ✓ 15. years-months-and-days ✓ 16. shapes ✓
17. comparing-and-number-properties ✓ 18. sorting-and-tables ✓

TW / Math は國小一年級〜國中九年級まで完了。次は下の「その後」から
tw のトピック別ページは `topic_defs_tw()`（topics.php、中国語の name・blurb、tw の slug 用の正規表現）。tw の単元を足したらどのトピックに入るか確認する
グラフ・物差しなど印刷で大きく出したい図は `<svg data-pf='lg' ...>` にする

US-TX / Math（Texas Essential Knowledge and Skills, TEKS §111.5 など）— country `us-tx`（name「Texas, USA」、lang en）、subject `math`、grade `grade-N`、Letter。生成スクリプトは `gen_ustx_math_gN_*`、共通部品は `tools/tx_common.py`（Texas の名前・地名、US の綴りと文法の自動修正 us_text、1,000 以上のカンマ自動付与、他国の生成スクリプトの問題関数を使う adopt・run・run_many、Kid・mcq・collect・letters・finish（他国の語の混入を LEAKS で検出）・make、strip_svg（strip diagram）・pv_chart_svg・words）。
US 英語・お金は $ と ¢（ペニーあり、$1・$5・$10・$20 札）。standard_code は TEKS のコード（例: 3.4F、複数は「3.3F, 3.3G」）、standard_text は TEKS 原文、standard_url は TEA の Chapter 111 Subchapter A。STAAR は Grade 3 から。重さは weight（mass と言わない）。多くの単元は US Common Core・Ontario・Australia の問題関数を Texas 向けに再利用（別の seed で別の問題になる）

US-TX / Math / Grade 3（STAAR の最初の学年）
1. place-value-to-100000 ✓ 2. comparing-and-ordering-numbers ✓ 3. rounding-and-estimating ✓ 4. adding-and-subtracting-within-1000 ✓ 5. multiplication-facts ✓
6. division-facts ✓ 7. multiplying-two-digit-by-one-digit ✓ 8. multiplication-and-division-word-problems ✓ 9. missing-factors-and-input-output-tables ✓ 10. odd-and-even-numbers ✓
11. fractions ✓ 12. fractions-on-a-number-line ✓ 13. equivalent-and-comparing-fractions ✓ 14. value-of-coins-and-bills ✓ 15. area ✓ 16. perimeter ✓
17. time-intervals ✓ 18. liquid-volume-and-weight ✓ 19. 2d-and-3d-figures ✓ 20. frequency-tables-dot-plots-and-bar-graphs ✓ 21. personal-financial-literacy ✓

US-TX / Math / Grade 4（STAAR の学年。1,000 以上はカンマ、10億まで）— 生成スクリプトは `gen_ustx_math_g4_*`（多くは US Grade 4 の問題関数を build_sets で再利用。他国の問題関数に People を渡すときはその生成スクリプトの People を使う）
1. place-value-to-billions ✓ 2. comparing-and-rounding-whole-numbers ✓ 3. decimals-tenths-and-hundredths ✓ 4. comparing-decimals-and-number-lines ✓ 5. adding-and-subtracting-whole-numbers-and-decimals ✓ 6. multiplying-by-10-and-100 ✓
7. multiplying-two-digit-numbers ✓ 8. multiplying-by-one-digit-numbers ✓ 9. long-division ✓ 10. estimating-with-rounding-and-compatible-numbers ✓ 11. multiplication-and-division-word-problems ✓ 12. multi-step-problems-and-strip-diagrams ✓
13. input-output-tables-and-number-patterns ✓ 14. decomposing-fractions ✓ 15. equivalent-and-comparing-fractions ✓ 16. adding-and-subtracting-fractions ✓ 17. area-and-perimeter-formulas ✓ 18. lines-angles-and-triangles ✓
19. lines-of-symmetry ✓ 20. measuring-angles ✓ 21. measurement-conversions ✓ 22. measurement-word-problems ✓ 23. frequency-tables-dot-plots-and-stem-and-leaf-plots ✓ 24. personal-financial-literacy ✓

US-TX / Math / Grade 5（STAAR の学年。小数は 1000 分の 1 まで）— 生成スクリプトは `gen_ustx_math_g5_*`（US Grade 5・Grade 4 の問題関数を build_sets で再利用、ほかは自前）。メートル法は mass（STAAR の参考資料と同じ）、ヤード・ポンド法は weight
1. decimal-place-value-to-thousandths ✓ 2. comparing-and-rounding-decimals ✓ 3. estimating ✓ 4. multiplying-three-digit-by-two-digit-numbers ✓ 5. dividing-by-two-digit-divisors ✓ 6. multiplying-decimals ✓
7. dividing-decimals ✓ 8. adding-and-subtracting-fractions ✓ 9. adding-and-subtracting-decimals ✓ 10. multiplying-whole-numbers-and-fractions ✓ 11. dividing-with-unit-fractions ✓ 12. prime-and-composite-numbers ✓
13. multi-step-problems-and-equations ✓ 14. numerical-patterns-and-graphs ✓ 15. order-of-operations ✓ 16. volume-of-rectangular-prisms ✓ 17. perimeter-area-and-volume-problems ✓ 18. classifying-two-dimensional-figures ✓
19. measurement-conversions ✓ 20. coordinate-plane ✓ 21. data-and-scatterplots ✓ 22. personal-financial-literacy ✓

US-TX / Math / Grade 6（STAAR の学年。負の数は「−」）— 生成スクリプトは `gen_ustx_math_g6_*`（US Grade 6・7 の問題関数を build_sets で再利用、ほかは自前）。standard_url は TEA の Chapter 111 Subchapter B（tx_common.make が Grade 6 以上で自動で切り替え）
1. integers-and-rational-numbers ✓ 2. comparing-and-ordering-rational-numbers ✓ 3. adding-and-subtracting-integers ✓ 4. multiplying-and-dividing-integers ✓ 5. dividing-fractions ✓
6. multiplying-and-dividing-decimals ✓ 7. ratios-and-rates ✓ 8. ratio-tables-and-graphs ✓ 9. fractions-decimals-and-percents ✓ 10. percent-problems ✓ 11. converting-units ✓
12. independent-and-dependent-quantities ✓ 13. exponents-and-order-of-operations ✓ 14. expressions-and-equations ✓ 15. equivalent-expressions ✓ 16. triangle-properties ✓
17. area-of-triangles-parallelograms-and-trapezoids ✓ 18. volume-of-rectangular-prisms ✓ 19. one-step-equations ✓ 20. one-step-inequalities ✓ 21. coordinate-plane ✓
22. dot-plots-histograms-and-box-plots ✓ 23. mean-median-range-and-iqr ✓ 24. categorical-data-and-relative-frequency ✓ 25. personal-financial-literacy ✓

US-TX / Math / Grade 7（STAAR の学年）— 生成スクリプトは `gen_ustx_math_g7_*`（US Grade 6〜8 の問題関数を build_sets で再利用。US Grade 7・8 の生成スクリプトはモジュールの R を使うので、新しい seed で R を入れ替える）。他の TX 生成スクリプトを import するときは imports に書く（extra に書くと GRADE が上書きされる）。tx_common.us_text は「an $8」などの冠詞も直す
1. sets-of-rational-numbers ✓ 2. adding-and-subtracting-rational-numbers ✓ 3. multiplying-and-dividing-rational-numbers ✓ 4. rational-number-word-problems ✓ 5. constant-rate-of-change ✓
6. unit-rates-with-fractions ✓ 7. constant-of-proportionality ✓ 8. percent-increase-and-decrease ✓ 9. converting-between-measurement-systems ✓ 10. similar-figures ✓ 11. scale-drawings ✓
12. circumference-and-area-of-circles ✓ 13. area-of-composite-figures ✓ 14. volume-of-prisms-and-pyramids ✓ 15. lateral-and-total-surface-area ✓ 16. linear-relationships ✓
17. two-step-equations ✓ 18. two-step-inequalities ✓ 19. equations-with-angles-and-triangles ✓ 20. probability-and-predictions ✓ 21. sample-spaces-and-compound-events ✓
22. random-samples-and-inferences ✓ 23. comparing-data-with-dot-plots-and-box-plots ✓ 24. sales-tax-income-tax-and-budgets ✓ 25. interest-net-worth-and-incentives ✓

US-TX / Math / Grade 8（STAAR の学年）— 生成スクリプトは `gen_ustx_math_g8_*`（US Grade 7・8 の問題関数を build_sets で再利用。Grade 7 と同じく R を新しい seed に入れ替える）。お金の教育（8.12）は 4 単元
1. sets-of-real-numbers ✓ 2. approximating-irrational-numbers ✓ 3. scientific-notation ✓ 4. ordering-real-numbers ✓ 5. dilations ✓ 6. slope ✓
7. proportional-and-non-proportional-relationships ✓ 8. writing-linear-equations ✓ 9. functions ✓ 10. scatterplots-and-trend-lines ✓ 11. equations-with-variables-on-both-sides ✓
12. systems-of-equations ✓ 13. angle-relationships-and-parallel-lines ✓ 14. transformations ✓ 15. pythagorean-theorem ✓ 16. distance-on-the-coordinate-plane ✓
17. volume-of-cylinders-cones-and-spheres ✓ 18. surface-area-of-prisms-and-cylinders ✓ 19. mean-absolute-deviation ✓ 20. random-samples-and-simulations ✓
21. cost-of-credit-and-loans ✓ 22. saving-and-investing-over-time ✓ 23. payment-methods-and-financial-responsibility ✓ 24. paying-for-college ✓

US-TX / Math / Grade 2（STAAR なし。1,200 まで。文は短く、絵を多く）— 生成スクリプトは `gen_ustx_math_g2_*`（US Grade 2・3、Ontario、AU の問題関数を build_sets で再利用、ほかは自前）。他国の A〜D の絵の問題（`build`・`_abcd`）は生成スクリプトの中で絵を作ってから渡す
1. place-value-to-1200 ✓ 2. comparing-and-ordering-numbers ✓ 3. number-lines ✓ 4. 10-more-10-less-100-more-100-less ✓ 5. addition-and-subtraction-facts-to-20 ✓
6. adding-and-subtracting-two-digit-numbers ✓ 7. adding-and-subtracting-within-1000 ✓ 8. word-problems-and-number-sentences ✓ 9. odd-and-even-numbers ✓ 10. counting-coins ✓
11. equal-groups-multiplication-and-division ✓ 12. halves-fourths-and-eighths ✓ 13. 2d-shapes-and-polygons ✓ 14. 3d-solids ✓ 15. measuring-length ✓ 16. length-word-problems ✓
17. area-with-square-units ✓ 18. telling-time-to-the-minute ✓ 19. pictographs-and-bar-graphs ✓ 20. personal-financial-literacy ✓

US-TX / Math / Grade 1（120 まで。とても短い文、絵を多く）— 生成スクリプトは `gen_ustx_math_g1_*`（US Grade 1・2、AU Year 1、Ontario、TX Grade 2 の問題関数を build_sets で再利用、ほかは自前）。AU の問題関数はオーストラリアの語（kookaburra・c の硬貨など）を keep で落とす
1. numbers-to-120 ✓ 2. comparing-and-ordering-numbers ✓ 3. adding-tens-and-ones ✓ 4. making-10 ✓ 5. addition-and-subtraction-facts-to-20 ✓
6. addition-and-subtraction-strategies ✓ 7. word-problems-within-20 ✓ 8. counting-coins ✓ 9. counting-to-120 ✓ 10. skip-counting-by-2s-5s-and-10s ✓
11. 10-more-and-10-less ✓ 12. equal-sign-and-missing-numbers ✓ 13. adding-three-numbers ✓ 14. 2d-shapes ✓ 15. 3d-solids ✓ 16. halves-and-fourths ✓
17. measuring-length ✓ 18. telling-time-to-the-hour-and-half-hour ✓ 19. tally-marks-and-graphs ✓ 20. personal-financial-literacy ✓

US-TX / Math / Kindergarten（5〜6歳。20 まで、数えるのは 100 まで。とても短い文、ほぼ全問に絵）— grade `kindergarten`（sort 0）。生成スクリプトは `gen_ustx_math_gk_*`（US Kindergarten・AU Foundation・US Grade 2・TX Grade 1 の問題関数を build_sets で再利用、ほかは自前）。自前の問題は pick() で場面を1回ずつ使い、名前だけ違う問題を作らない。tx_common.us_text は ladybird→ladybug、kookaburra→robin も直す
1. counting-to-20 ✓ 2. reading-and-writing-numbers-0-to-20 ✓ 3. subitizing ✓ 4. one-more-and-one-less ✓ 5. comparing-numbers-to-20 ✓ 6. composing-and-decomposing-numbers-to-10 ✓
7. addition-within-10 ✓ 8. subtraction-within-10 ✓ 9. addition-and-subtraction-strategies ✓ 10. counting-to-100-by-ones-and-tens ✓ 11. naming-coins ✓ 12. 2d-shapes ✓
13. 3d-solids ✓ 14. comparing-length-capacity-and-weight ✓ 15. sorting-and-picture-graphs ✓ 16. personal-financial-literacy ✓

US-TX / Math / Algebra I（TEKS §111.39、STAAR Algebra I の科目。高校）— grade `algebra-1`（name「Algebra I」、sort 9）。standard_url は TEA の Chapter 111 Subchapter C（tx_common.make が algebra で自動で切り替え）。生成スクリプトは `gen_ustx_math_a1_*`（US Algebra 1・Algebra 2・Geometry・Grade 8 の問題関数を build_sets で再利用、ほかは自前）。US の固定の文章題（problems()）は半分（10問）だけ使い、残りは別の問題関数で埋める。domain は TEKS の分野名（Linear Functions, Equations, and Inequalities／Quadratic Functions and Equations／Exponential Functions and Equations／Number and Algebraic Methods／Algebraic Reasoning）
1. functions-and-function-notation ✓ 2. domain-and-range ✓ 3. slope-and-rate-of-change ✓ 4. graphing-linear-functions ✓ 5. writing-linear-equations ✓ 6. parallel-and-perpendicular-lines ✓
7. direct-variation ✓ 8. solving-linear-equations ✓ 9. linear-inequalities ✓ 10. systems-of-linear-equations ✓ 11. systems-of-linear-inequalities ✓ 12. correlation-and-lines-of-fit ✓
13. transformations-of-linear-functions ✓ 14. polynomial-operations ✓ 15. dividing-polynomials ✓ 16. factoring ✓ 17. graphing-quadratic-functions ✓ 18. writing-quadratic-functions ✓
19. transformations-of-quadratic-functions ✓ 20. solving-quadratic-equations ✓ 21. exponential-functions ✓ 22. exponents-and-radicals ✓ 23. arithmetic-and-geometric-sequences ✓ 24. literal-equations-and-formulas ✓

US-TX / Math / Geometry（TEKS §111.41。高校）— grade `geometry`（name「Geometry」、sort 10）。standard_url は Subchapter C（tx_common.make は grade- 以外を ch111c にする）。生成スクリプトは `gen_ustx_math_ge_*`（US Geometry・Precalculus・Grade 7、TX Grade 8、AU Year 8 の問題関数を build_sets で再利用、ほかは自前）。domain は TEKS の分野名（Coordinate and Transformational Geometry／Logical Argument and Constructions／Proof and Congruence／Similarity, Proof, and Trigonometry／Two-Dimensional and Three-Dimensional Figures／Circles／Probability）。tx_common.us_text は trapezium→trapezoid も直す
1. points-lines-planes-and-definitions ✓ 2. conditional-statements-and-counterexamples ✓ 3. segments-midpoints-and-partitions ✓ 4. distance-slope-and-midpoint-formulas ✓ 5. equations-of-parallel-and-perpendicular-lines ✓
6. angles-and-parallel-lines ✓ 7. transformations ✓ 8. reflectional-and-rotational-symmetry ✓ 9. triangle-angle-theorems ✓ 10. triangle-inequality-theorem ✓ 11. proving-triangles-congruent ✓
12. midsegments-bisectors-and-medians ✓ 13. quadrilaterals-and-polygon-angles ✓ 14. dilations-and-similar-figures ✓ 15. similar-triangles-and-proportionality ✓ 16. right-triangle-similarity-and-geometric-mean ✓
17. pythagorean-theorem-and-special-right-triangles ✓ 18. trigonometric-ratios ✓ 19. cross-sections-and-solids-of-revolution ✓ 20. dimensional-change ✓ 21. area-of-regular-polygons-and-composite-figures ✓
22. surface-area ✓ 23. volume ✓ 24. circle-angles-chords-tangents-and-secants ✓ 25. arc-length-sector-area-and-radians ✓ 26. equations-of-circles ✓ 27. permutations-and-combinations ✓
28. geometric-probability ✓ 29. independent-and-conditional-probability ✓

US-TX / Math / Algebra II（TEKS §111.40。高校）— grade `algebra-2`（name「Algebra II」、sort 11）。standard_url は Subchapter C。生成スクリプトは `gen_ustx_math_a2_*`（US Algebra 1・Algebra 2・Precalculus の問題関数を build_sets で再利用、ほかは自前）。TX Algebra I で使った US の固定の文章題（problems()）は使わない。親関数の変形は `fam(tr.one_x, "sqrt")` で US Algebra 2 の PARENTS を絞り、1/x・∛x・b^x・log_b x（b は 2・10・e）は自前の `tf(kind)`、f(bx) は自前の `one_bx_maker`。domain は TEKS の分野名（Attributes of Functions and Their Inverses／Systems of Equations and Inequalities／Quadratic and Square Root Functions, Equations, and Inequalities／Exponential and Logarithmic Functions and Equations／Cubic, Cube Root, Absolute Value, and Rational Functions, Equations, and Inequalities／Number and Algebraic Methods／Data）。年（2015 など）は自動でカンマが付くので文章題に書かない
1. parent-functions ✓ 2. inverse-functions ✓ 3. domain-and-range-notation ✓ 4. systems-of-three-equations ✓ 5. linear-quadratic-systems ✓ 6. systems-of-linear-inequalities ✓
7. quadratic-through-three-points ✓ 8. parabolas-focus-and-directrix ✓ 9. completing-the-square-and-vertex-form ✓ 10. quadratic-equations-and-inequalities ✓ 11. square-root-functions-and-equations ✓ 12. exponential-and-logarithmic-functions ✓
13. logarithms ✓ 14. exponential-and-logarithmic-equations ✓ 15. cubic-and-cube-root-functions ✓ 16. absolute-value-functions-equations-and-inequalities ✓ 17. rational-functions ✓ 18. rational-equations-and-inverse-variation ✓
19. complex-numbers ✓ 20. polynomial-operations-and-division ✓ 21. factoring-polynomials ✓ 22. rational-expressions ✓ 23. radicals-and-rational-exponents ✓ 24. data-and-regression ✓

US-TX / Math / Precalculus（TEKS §111.42。高校）— grade `precalculus`（name「Precalculus」、sort 12）。standard_code は「P.2A」形式。生成スクリプトは `gen_ustx_math_pc_*`（US Algebra 2・Precalculus・Geometry の問題関数を build_sets で再利用、ほかは自前）。TX Algebra II・Geometry で使った問題関数は、できるだけ別の問題関数か自前に替える。domain は TEKS の分野名（Functions／Relations and Geometric Reasoning／Number and Measure／Algebraic Reasoning）。不等式の区間表記は自前の `solve_ineq`（pc の生成スクリプト内）
1. composition-of-functions ✓ 2. even-odd-and-inverse-functions ✓ 3. piecewise-and-step-functions ✓ 4. transformations-of-functions ✓ 5. key-features-of-polynomial-functions ✓ 6. end-behavior ✓ 7. asymptotes-of-rational-functions ✓
8. discontinuities ✓ 9. modeling-with-functions ✓ 10. trigonometric-values-of-special-angles ✓ 11. degrees-radians-and-reference-angles ✓ 12. linear-and-angular-velocity ✓ 13. graphs-of-trigonometric-functions ✓ 14. sinusoidal-models ✓
15. inverse-trigonometric-functions ✓ 16. trigonometric-identities ✓ 17. trigonometric-equations ✓ 18. bearings-and-angles-of-elevation ✓ 19. law-of-sines-and-law-of-cosines ✓ 20. vectors ✓ 21. parametric-equations ✓
22. polar-coordinates-and-graphs ✓ 23. conic-sections ✓ 24. ellipses-and-hyperbolas ✓ 25. sequences-series-and-sigma-notation ✓ 26. logarithmic-and-exponential-equations ✓ 27. polynomial-equations-and-inequalities ✓ 28. rational-inequalities ✓

US-TX / Math は Kindergarten〜Precalculus まで完了。ws_common.num は割り切れない小数で None を返すので、選択肢の文字列に入れるときは `num(x) or num(x, "f")` にする

PH / Math（DepEd MATATAG Curriculum, Mathematics）— country `ph`（name「Philippines」、lang en、hreflang en-ph）、subject `math`、grade `grade-N`、Letter。生成スクリプトは `gen_ph_math_gN_*`、共通部品は `tools/ph_common.py`（tx_common と同じ API。フィリピンの名前・地名、localize で他国の生成スクリプトの名前をフィリピンの名前に置き換え、us_text で US の綴り（round→around、ml→mL、a.m.. の重複も直す）、LEAKS で $・¢・£・inch・miles・Texas などの混入を落とす、peso（₱25、₱1,250、₱45.50）、make）。
US 英語・メートル法だけ・お金は ₱ と centavos（25 centavos 硬貨・₱1 硬貨・₱50〜₱1,000 札）。時刻は「9:30 a.m.」。1,000 以上はカンマ（DepEd の CG は空白区切りだがカンマを使う）。場面はフィリピン（sari-sari store、jeepney、pandesal、Carabao mango、Cebu、Davao）。
standard_code は MATATAG の分野名「Grade 4: Number and Algebra」／「Grade 4: Measurement and Geometry」／「Grade 4: Data and Probability」、standard_text は CG の learning competency の原文、standard_url は Grade 1・4・7 は CG の PDF（ph_common.STD_URLS）。年齢は US と同じ（Grade N = N+5〜N+6 歳、unit.php）。
Grade 4 の分数は CG のとおり分母 10 まで（他国の問題関数は keep の den10・den_q10 で絞る）

PH / Math / Grade 4（MATATAG。Q1〜Q4 の順）
1. angles ✓ 2. triangles-and-quadrilaterals ✓ 3. perimeter ✓ 4. numbers-up-to-1000000 ✓ 5. rounding-and-estimating ✓ 6. adding-and-subtracting-to-1000000 ✓
7. multiplying-whole-numbers ✓ 8. dividing-whole-numbers ✓ 9. multi-step-word-problems-and-money ✓ 10. order-of-operations-mdas ✓ 11. proper-improper-fractions-and-mixed-numbers ✓
12. adding-and-subtracting-similar-fractions ✓ 13. converting-units-of-length-mass-and-capacity ✓ 14. converting-time-and-elapsed-time ✓ 15. comparing-and-ordering-dissimilar-fractions ✓
16. equivalent-fractions-and-simplest-form ✓ 17. factors-and-multiples ✓ 18. adding-and-subtracting-dissimilar-fractions ✓ 19. line-symmetry ✓ 20. reflection-and-glide-reflection ✓
21. decimal-numbers-to-hundredths ✓ 22. comparing-ordering-and-rounding-decimals ✓ 23. patterns ✓ 24. number-sentences-properties-and-equivalent-facts ✓ 25. tables-and-line-graphs ✓

PH / Math / Grade 7（MATATAG。高校の最初の学年）— 生成スクリプトは `gen_ph_math_g7_*`。UK KS3・AU Year 7–8・SG Sec・US Grade 6–8・TX・Ontario・BC の問題関数（one_x・set_x）を再利用。
ph_common.adopt は gbp・aud・sgd などのお金の関数を peso に替える（モジュール独自の money は imports の extra で `mod.money = peso`）。単位換算の単元だけ `ph_common.ALLOW_IMPERIAL = True`（CG が across different systems のため）。
LEAKS にカナダ・オーストラリア・英国・米国の地名と雪のスポーツを入れてある。新しく混ざったら LEAKS に足す。VAT は 12%。「standard form」は「decimal form」に直す
1. classifying-and-drawing-polygons ✓ 2. angle-pairs ✓ 3. interior-and-exterior-angles-of-polygons ✓ 4. percentage-increase-and-decrease ✓ 5. discount-commission-vat-and-simple-interest ✓
6. budgets-and-financial-plans ✓ 7. rates-and-speed ✓ 8. fractions-decimals-and-percentages ✓ 9. ordering-rational-numbers-on-a-number-line ✓ 10. operations-on-rational-numbers ✓
11. square-roots-and-cube-roots ✓ 12. irrational-numbers-on-the-number-line ✓ 13. sets-subsets-union-and-intersection ✓ 14. subsets-of-real-numbers ✓ 15. converting-units-of-measure ✓
16. volume-of-cylinders ✓ 17. volume-of-pyramids ✓ 18. data-collection-and-sampling ✓ 19. frequency-distribution-tables ✓ 20. statistical-graphs ✓
21. integers-and-absolute-value ✓ 22. adding-and-subtracting-integers ✓ 23. multiplying-and-dividing-integers ✓ 24. order-of-operations-gemdas ✓
25. algebraic-expressions ✓ 26. properties-of-equality-and-solving-equations ✓ 27. formulas-and-solving-for-a-variable ✓ 28. scientific-notation ✓ 29. probability-experiments-and-outcomes ✓

PH / Math / Grade 1（MATATAG。100 まで、計算は 20 まで・100 までは繰り上がり／繰り下がりなし。とても短い文、ほぼ全問に絵）— 生成スクリプトは `gen_ph_math_g1_*`。US Grade 1・AU Year 1／Foundation・UK Year 1・SG Primary 1・Ontario・BC・TX Grade 1・AU Year 2（turns・time）の問題関数を再利用。
120 までの問題関数は keep の le100 で絞る。足し算の単元は add20（引き算の話を落とす）。お金は自前の money_svg（₱1・₱5・₱10・₱20 硬貨、₱20・₱50・₱100 札、centavo なし）。
ph_common.run_many は A〜D の絵の問題（"build"）を組み立ててから使う。pence（5p）・puck も LEAKS
1. 2d-shapes ✓ 2. composing-and-decomposing-shapes ✓ 3. counting-to-100 ✓ 4. reading-and-writing-numbers-to-100 ✓ 5. comparing-and-ordering-numbers-to-20 ✓ 6. ordinal-numbers ✓
7. composing-and-decomposing-numbers-to-10 ✓ 8. addition-within-20 ✓ 9. addition-word-problems-within-20 ✓ 10. measuring-length-with-non-standard-units ✓ 11. ordering-numbers-to-100 ✓
12. skip-counting-by-2s-5s-and-10s ✓ 13. tens-and-ones ✓ 14. adding-within-100-without-regrouping ✓ 15. pictographs ✓ 16. subtraction-within-20 ✓
17. missing-numbers-and-equivalent-expressions ✓ 18. subtracting-within-100-without-regrouping ✓ 19. repeating-patterns ✓ 20. halves-and-quarters ✓
21. philippine-money ✓ 22. half-turns-and-quarter-turns ✓ 23. telling-time ✓ 24. days-of-the-week-and-months-of-the-year ✓

PH の次: MATATAG の CG が出ている学年（1・4・7）は完了。Grades 2・3・5・6・8 は CG が公開されたら（DepEd の MATATAG ページを確認）。catalog.json に学年を足す

ZA / Maths（CAPS Mathematics。Intermediate Phase は Grade 4–6）— country `za`（name「South Africa」、lang en、hreflang en-za）、subject `maths`、grade `grade-N`、A4。生成スクリプトは `gen_za_maths_gN_*`、共通部品は `tools/za_common.py`（ph_common と同じ API。南アの名前・地名、localize、gb_text でイギリス式の綴り（colour・metre・trapezium・anti-clockwise・maths・learners・tuck shop・spaza shop・biscuits・sweets）、LEAKS で $・₱・£・inch・Texas・フィリピンや英国の地名などを落とす、rand（R25、R1 250、R45,50）・cents（50c）、make）。
数の書き方は南ア式: 1 000 以上は空白区切り（4 536、10 000。ノーブレークスペース）、小数はコンマ（2,5・R12,50）。za_numbers が SVG の文字も含めて自動で直す（小数が並ぶときは「1,5; 2,5」）。容量は mℓ と ℓ。時刻は 24 時間制「14:30」も使う。
standard_code は CAPS の topic「Grade 4: 1.1 Whole numbers」形式、standard_text は CAPS の concepts and skills の要約、standard_url は CAPS IP Mathematics Gr 4-6 の PDF。domain は CAPS の 5 分野（Numbers, Operations and Relationships／Patterns, Functions and Algebra／Space and Shape (Geometry)／Measurement／Data Handling）。年齢は US と同じ（unit.php）。topic_gb() に za を入れた
Grade 4 の分数は CAPS のとおり halves〜eighths（keep の den8。同値分数は den12）。数は 10 000 まで（le10000）

ZA / Maths / Grade 4（CAPS）
1. whole-numbers-to-10000 ✓ 2. rounding-off-to-10-100-and-1000 ✓ 3. addition-and-subtraction ✓ 4. calculation-techniques ✓ 5. multiplication-tables-to-10-x-10 ✓ 6. multiplication ✓
7. division ✓ 8. multiples-and-factors ✓ 9. properties-of-operations ✓ 10. common-fractions ✓ 11. money-rate-and-ratio-problems ✓ 12. numeric-patterns ✓ 13. geometric-patterns ✓
14. number-sentences ✓ 15. 2d-shapes-and-angles ✓ 16. 3d-objects ✓ 17. symmetry ✓ 18. composite-shapes-and-tessellations ✓ 19. viewing-objects ✓ 20. position-and-movement ✓
21. length ✓ 22. mass ✓ 23. capacity-and-volume ✓ 24. time ✓ 25. temperature ✓ 26. perimeter-area-and-volume ✓ 27. collecting-and-organising-data ✓
28. pictographs-bar-graphs-and-pie-charts ✓ 29. probability ✓

ZA / Maths / Grade 5（CAPS。数は 6 桁まで、小数なし（お金の R45,50 だけ）、分数は twelfths まで、温度は正の数だけ）— 生成スクリプトは `gen_za_maths_g5_*`。G4 の生成スクリプトの問題関数（換算・お金・温度など）も再利用。za_common.gb_text は ZA_PLACES で AU の動物・米国の鳥・Sydney・fall も南ア向けに直す
1. whole-numbers-to-6-digits ✓ 2. rounding-off-to-5-10-100-and-1000 ✓ 3. addition-and-subtraction ✓ 4. calculation-techniques ✓ 5. multiplication ✓ 6. division ✓ 7. multiples-and-factors ✓ 8. properties-of-operations ✓ 9. common-fractions ✓ 10. adding-and-subtracting-fractions ✓ 11. money-rate-and-ratio-problems ✓ 12. numeric-patterns ✓ 13. geometric-patterns ✓ 14. number-sentences ✓ 15. 2d-shapes ✓ 16. angles ✓ 17. 3d-objects ✓ 18. symmetry ✓ 19. transformations ✓ 20. viewing-objects ✓ 21. position-and-movement ✓ 22. length ✓ 23. mass ✓ 24. capacity-and-volume ✓ 25. time ✓ 26. temperature ✓ 27. perimeter-area-and-volume ✓ 28. collecting-and-organising-data ✓ 29. pictographs-bar-graphs-and-pie-charts ✓ 30. probability ✓

ZA / Maths / Grade 6（CAPS。数は 9 桁まで、小数は 3 桁まで（コンマ）、負の数なし、分数は twelfths まで＋100分の1）— 生成スクリプトは `gen_za_maths_g6_*`。時刻表は自前（Gautrain・MyCiTi・Metrorail・Durban bus）。za_ok は SVG の文字と aria-label も LEAKS で調べる（AU・カナダの地名や動物、maple）。gb_text は Year N→Grade N、Pupil・Student→Learner、Fall→Autumn も直す
1. whole-numbers-to-9-digits ✓ 2. rounding-off ✓ 3. addition-and-subtraction ✓ 4. calculation-techniques ✓ 5. multiplication ✓ 6. division ✓ 7. multiples-factors-and-prime-numbers ✓ 8. properties-and-order-of-operations ✓ 9. common-fractions ✓ 10. adding-and-subtracting-fractions ✓ 11. fractions-of-whole-numbers ✓ 12. decimal-fractions ✓ 13. adding-and-subtracting-decimals ✓ 14. multiplying-and-dividing-decimals ✓ 15. percentages ✓ 16. money-rate-and-ratio-problems ✓ 17. numeric-patterns ✓ 18. geometric-patterns ✓ 19. number-sentences ✓ 20. 2d-shapes ✓ 21. angles ✓ 22. 3d-objects ✓ 23. symmetry ✓ 24. transformations-enlargements-and-reductions ✓ 25. position-and-movement ✓ 26. length ✓ 27. mass ✓ 28. capacity-and-volume ✓ 29. time ✓ 30. temperature ✓ 31. perimeter-area-and-volume ✓ 32. collecting-and-organising-data ✓ 33. pictographs-bar-graphs-and-pie-charts ✓ 34. probability ✓

ZA / Maths / Grade 7（CAPS Senior Phase。負の数は「−」、円・π・指数表記は Grade 8 以降なので出さない（keep の ok7））— 生成スクリプトは `gen_za_maths_g7_*`。UK Year 7・AU Year 7 の one_x を collect で多く再利用。standard_url は CAPS SP Mathematics Gr 7-9 の PDF（STD_URL_SP）。
Senior Phase は `za_common.GBP_TO_RAND = True`（UK・AU の問題関数の £・$ を R に、pence を cents に）。za_ok は GST・HST と 15% 以外の VAT を落とす。gb_text は mom→mother。財務（利益・割引・VAT 15%・予算・単利）は自前
1. whole-numbers ✓ 2. multiples-factors-and-prime-factorisation ✓ 3. calculating-with-whole-numbers ✓ 4. ratio-and-rate ✓ 5. financial-maths ✓ 6. exponents ✓ 7. integers ✓ 8. common-fractions ✓ 9. multiplying-fractions ✓ 10. percentages ✓ 11. decimal-fractions ✓ 12. calculating-with-decimals ✓ 13. numeric-and-geometric-patterns ✓ 14. functions-and-relationships ✓ 15. algebraic-expressions ✓ 16. algebraic-equations ✓ 17. graphs ✓ 18. geometry-of-straight-lines ✓ 19. triangles-and-quadrilaterals ✓ 20. 3d-objects ✓ 21. transformation-geometry ✓ 22. area-and-perimeter ✓ 23. surface-area-and-volume ✓ 24. collecting-and-summarising-data ✓ 25. bar-graphs-histograms-and-pie-charts ✓ 26. probability ✓

ZA / Maths / Grade 8（CAPS Senior Phase。円・π・指数表記・ピタゴラスあり。三角比・二次方程式はなし（keep の ok8））— 生成スクリプトは `gen_za_maths_g8_*`。UK Year 7–9・AU Year 7–8・SG Sec 1 の one_x を再利用。財務（割賦・複利・為替）は自前（為替は「Suppose 1 euro = R20」の形で dollar を使わない）。
za_common: gb_text は standard form→scientific notation、za_ok は「= None」の壊れた解説を落とす、collect は ValueError なども飛ばす
1. whole-numbers ✓ 2. financial-maths ✓ 3. integers ✓ 4. exponents ✓ 5. scientific-notation ✓ 6. common-fractions ✓ 7. decimal-fractions ✓ 8. numeric-and-geometric-patterns ✓ 9. functions-and-relationships ✓ 10. algebraic-expressions ✓ 11. algebraic-equations ✓ 12. graphs ✓ 13. geometry-of-straight-lines ✓ 14. triangles-congruence-and-similarity ✓ 15. quadrilaterals-and-polygons ✓ 16. transformation-geometry ✓ 17. 3d-objects ✓ 18. area-and-perimeter ✓ 19. surface-area-and-volume ✓ 20. theorem-of-pythagoras ✓ 21. collecting-and-summarising-data ✓ 22. histograms-pie-charts-and-line-graphs ✓ 23. probability ✓

ZA / Maths / Grade 9（CAPS Senior Phase。負の指数・因数分解（共通因数・平方の差・三項式）・因数分解で解く方程式・指数方程式・円柱あり。三角比・連立方程式・円錐・球はなし（keep の ok9））— 生成スクリプトは `gen_za_maths_g9_*`。SG Sec 1–3・UK Year 8–9・AU Year 8 の one_x を再利用。手数料・家賃は自前、複利・割賦・為替は G8 の問題関数
1. real-numbers ✓ 2. financial-maths ✓ 3. exponents ✓ 4. scientific-notation ✓ 5. numeric-and-geometric-patterns ✓ 6. functions-and-relationships ✓ 7. algebraic-expressions ✓ 8. factorisation ✓ 9. algebraic-equations ✓ 10. linear-graphs ✓ 11. geometry-of-straight-lines ✓ 12. similar-and-congruent-triangles ✓ 13. quadrilaterals-and-polygons ✓ 14. transformation-geometry ✓ 15. 3d-objects-views-and-nets ✓ 16. area-and-perimeter ✓ 17. surface-area-and-volume ✓ 18. theorem-of-pythagoras ✓ 19. collecting-and-summarising-data ✓ 20. scatter-plots-histograms-and-pie-charts ✓ 21. probability ✓

ZA / Maths / Grade 10（CAPS FET Phase。standard_url は CAPS FET Mathematics Gr 10-12 の PDF（STD_URL_FET）。三角比は 0°〜360°、三角方程式は 0°〜90°。複素数・対数・弧度法・正弦／余弦定理・独立事象・有理指数はなし（keep の ok10））— 生成スクリプトは `gen_za_maths_g10_*`。US Algebra 1・Geometry、UK Year 8–9、SG Sec 1–4、AU Year 7–8 の one_x を再利用。特別角・三角方程式・三角関数のグラフ・y = ax² + q・y = a/x + q・y = abˣ + q・逆数比・P(x; y)・単利・インフレ・排反／余事象は自前。
domain は「Algebra and Number Patterns／Functions／Trigonometry／Euclidean and Analytical Geometry／Finance and Growth／Measurement／Statistics and Probability」。
za_common.gb_text（GBP_TO_RAND のとき）は座標 (3, 4)→(3; 4)、m∠→∠、slope→gradient、penny→cent も直す
1. number-system-and-surds ✓ 2. products-and-factorisation ✓ 3. algebraic-fractions ✓ 4. exponents-and-exponential-equations ✓ 5. number-patterns ✓ 6. linear-and-literal-equations ✓ 7. quadratic-equations ✓ 8. simultaneous-equations ✓ 9. linear-inequalities ✓ 10. trigonometric-ratios ✓ 11. special-angles-equations-and-2d-problems ✓ 12. trigonometric-functions ✓ 13. linear-and-quadratic-functions ✓ 14. hyperbolic-and-exponential-functions ✓ 15. euclidean-geometry ✓ 16. analytical-geometry ✓ 17. finance-and-growth ✓ 18. statistics ✓ 19. measurement ✓ 20. probability ✓

ZA / Maths / Grade 11（CAPS FET Phase。対数・弧度法・sec/csc/cot・複合角／2倍角・微分はなし（kp(ok11) で他国の問題関数を絞る））— 生成スクリプトは `gen_za_maths_g11_*`。US Algebra 1・Geometry、SG Sec 3–4、UK Year 8–9、TX Algebra II の one_x を kp() で再利用。判別式・二次不等式・二次数列・接線・傾斜角・y = a(x + p)² + q・y = a/(x + p) + q・y = ab^(x + p) + q・k と p の三角関数グラフ・還元公式・恒等式・一般解・減価償却・実効金利は自前（fk(fun, kind) は種類ごとに 1 つの uniq を共有して、セットをまたいで同じ問題を出さない）。
za_common.gb_text は Law of Sines→Sine rule、perpendicular slopes→perpendicular gradients も直す
1. exponents-and-surds ✓ 2. completing-the-square-and-quadratic-formula ✓ 3. nature-of-roots ✓ 4. quadratic-inequalities ✓ 5. simultaneous-linear-and-quadratic-equations ✓ 6. quadratic-number-patterns ✓ 7. analytical-geometry ✓ 8. quadratic-functions ✓ 9. hyperbolic-and-exponential-functions ✓ 10. trigonometric-functions ✓ 11. reduction-formulae-and-identities ✓ 12. trigonometric-equations ✓ 13. sine-cosine-and-area-rules ✓ 14. euclidean-geometry-circle-theorems ✓ 15. finance-growth-and-decay ✓ 16. probability ✓ 17. statistics ✓

ZA / Maths / Grade 12（CAPS FET Phase、NSC（matric）の学年。弧度法・sec/csc/cot・tan の複合角・nCr・ln/e・積分はなし（kp(ok12)）。kp() は関数ごとに 1 つの uniq を共有し、localize・gb_text 後の文で重複を判定する）— 生成スクリプトは `gen_za_maths_g12_*`。US Algebra 2・Precalculus・Geometry・Algebra 1、SG Sec 4 の one_x を kp() で再利用。年金（将来価値・現在価値・返済額・回数・減債基金）、微分（極限・定義・公式・接線・三次関数・最適化・速度）、数列の和・Σ・無限和、逆関数、対数、円の接線、比例定理、回帰、数え上げは自前。
南アの小数は小数点以下 3 桁がちょうど 3 桁だと za_numbers が千の位の区切りと見なす（0,075 → 0 075）ので、利率は「7,5% ÷ 12」、和は分数で書く。トピック `calculus`（Differential Calculus）を足した
1. arithmetic-and-geometric-sequences-and-series ✓ 2. sigma-notation-and-sum-to-infinity ✓ 3. inverse-functions ✓ 4. logarithms ✓ 5. future-value-annuities-and-sinking-funds ✓ 6. present-value-annuities-and-loans ✓ 7. factor-theorem-and-cubic-polynomials ✓ 8. limits-and-first-principles ✓ 9. rules-of-differentiation ✓ 10. equations-of-tangents ✓ 11. cubic-functions ✓ 12. optimisation-and-rates-of-change ✓ 13. compound-and-double-angles ✓ 14. problems-in-three-dimensions ✓ 15. analytical-geometry-circles ✓ 16. euclidean-geometry-proportionality-and-similarity ✓ 17. regression-and-correlation ✓ 18. counting-principle-and-probability ✓

ZA / Maths / Grade 1–3（CAPS Foundation Phase。standard_url は CAPS FP Mathematics Gr 1-3 の PDF（STD_URL_FP）。G1 は 20 まで（数えるのは 100 まで）、G2 は 99 まで（数えるのは 200 まで）、G3 は 999 まで。とても短い文、絵を多く）— 生成スクリプトは `gen_za_maths_g1_*`・`g2_*`・`g3_*`。
数・計算・文章題・かけ算わり算は自前（num_k・calc_k・story_k・group_k を F(fun, kind, 範囲) で使う。k_pics の絵）、お金は自前（mk(kind, 上限の cents)、10c〜R5 の硬貨と R10〜R200 の札の絵）。図形・位置・時刻・測定・データ・分数・パターンは UK Year 1–3・AU Year 1–3・Ontario Grade 1–3・US Grade 1 のセット関数を run で再利用（le(n) で数の上限、nomoney でお金の問題を落とす）。
za_common: adopt は大文字で始まる地名のリストだけを南アの地名に替える（tree・house などはそのまま）、za_ok は名前や語を置き換えたあとで選択肢が重なる問題を落とす、conkers→marbles、loonies・snowbank などを LEAKS に
ZA / Maths / Grade 1
1. counting-to-100 ✓ 2. numbers-to-20 ✓ 3. tens-and-ones ✓ 4. number-bonds-to-10 ✓ 5. addition-and-subtraction-to-20 ✓ 6. problem-solving-to-20 ✓ 7. grouping-and-sharing ✓ 8. halves-and-quarters ✓ 9. money ✓ 10. patterns ✓ 11. 2d-shapes-and-3d-objects ✓ 12. position-and-direction ✓ 13. time ✓ 14. length-mass-and-capacity ✓ 15. data-handling ✓
ZA / Maths / Grade 2
1. numbers-to-200 ✓ 2. place-value ✓ 3. odd-and-even-numbers ✓ 4. addition-and-subtraction-facts-to-20 ✓ 5. adding-and-subtracting-to-99 ✓ 6. problem-solving-to-99 ✓ 7. multiplication-by-2-5-and-10 ✓ 8. sharing-and-grouping ✓ 9. fractions ✓ 10. money ✓ 11. patterns ✓ 12. 2d-shapes-3d-objects-and-symmetry ✓ 13. position-and-direction ✓ 14. time ✓ 15. length-mass-and-capacity ✓ 16. data-handling ✓
ZA / Maths / Grade 3
1. numbers-to-1000 ✓ 2. place-value ✓ 3. adding-and-subtracting-to-999 ✓ 4. mental-mathematics ✓ 5. problem-solving-to-999 ✓ 6. times-tables-2-3-4-5-and-10 ✓ 7. multiplication-and-division ✓ 8. fractions ✓ 9. money ✓ 10. patterns ✓ 11. 2d-shapes-and-3d-objects ✓ 12. symmetry ✓ 13. position-and-maps ✓ 14. time ✓ 15. length ✓ 16. mass-and-capacity ✓ 17. perimeter-and-area ✓ 18. data-handling ✓

ZA / Maths / Grade R（Reception Year、5〜6歳）— grade `grade-r`（name「Grade R」、sort 0）。standard_url は CAPS Gr R の PDF（STD_URL_R）。10 まで、とても短い文、ほぼ全問に絵。お金（認識だけ）・かけ算わり算はなし。生成スクリプトは `gen_za_maths_gr_*`。US Kindergarten・AU Foundation・SG Primary 1（ordinal）・UK Year 1・US Grade 1 の問題関数を再利用、数・文章題・分ける問題は自前（FC で 10 を超える誤答を近い数に替え、÷ を使わない）。le は「1 cats」のような文法の誤り・kaya などの混入も落とす。図形は circle・triangle・square・rectangle・ball・box だけを答えにする（basic）。unit.php で educationalLevel を Grade R / Reception Year に
1. counting-to-10 ✓ 2. number-symbols-and-names-to-10 ✓ 3. comparing-and-ordering-to-10 ✓ 4. ordinal-numbers-to-tenth ✓ 5. adding-and-taking-away-to-10 ✓ 6. story-sums-to-10 ✓ 7. sharing-and-halves ✓ 8. patterns ✓ 9. 2d-shapes-and-3d-objects ✓ 10. position-and-direction ✓ 11. time ✓ 12. length-mass-and-capacity ✓ 13. sorting-and-data ✓

ZA / Maths は Grade R〜12 まで完了

DE / Mathe（KMK-Bildungsstandards Mathematik Primarbereich, Fassung 2022。学年への配分は各州の Lehrplan の一般的な内容）— country `de`（name「Deutschland」、lang `de`、hreflang de-de）、subject `mathe`（Mathe）、grade `klasse-N`（Klasse N、N+5〜N+6 歳）、A4。生成スクリプトは `gen_de_mathe_kN_*`、共通部品は `tools/de_common.py`（num・dez・eur（3,50 €・45 ct）・Kids（名前と er/sie）・mcq・mix・lesson・example・make_unit・schriftlich（Karopapier の筆算）・zahlenstrahl・dienes・stellenwerttafel・saeulen・strichliste・geld_svg・solid_svg・clock）。
ドイツ語、du で話しかける短い文。記号は 3 · 4（Malpunkt）、12 : 3、17 : 5 = 3 Rest 2。小数はコンマ（2,50 €）、5 桁以上はノーブレークスペース区切り。時刻は「8:15 Uhr」、時間量は「1 h 25 min」。「halb vier」= 3:30 Uhr。
domain は Leitidee（Zahl und Operation／Raum und Form／Muster, Strukturen und funktionaler Zusammenhang／Größen und Messen／Daten und Zufall）、standard_code は「Leitidee Zahl und Operation」、standard_text は要約、standard_url は KMK の Primarbereich Mathe PDF。body_html は「So geht's → Beispiel → Typische Fehler」。
q・c・e の中の < > は &lt; &gt;（faq・standard_text・key は生の < >）。数・名詞の単数（1 Kästchen はよいが 1 Stücke は不可）に注意。
サイトの UI 文言は core.php の 'de'（T と js_text。js の桁区切りは sep = '.'）、学年＋教科の語順は gs()（「Mathe Klasse 3」）、英語の小文字化は lc()。トピックは topics.php の `topic_defs_de()`（ドイツ語の slug 用）。topic.php・topics.php に $de の文言がある

DE / Mathe / Klasse 3
1. zahlen-bis-1000 ✓ 2. zahlen-vergleichen-und-ordnen ✓ 3. runden-und-ueberschlagen ✓ 4. plus-und-minus-bis-1000 ✓ 5. schriftliche-addition ✓ 6. schriftliche-subtraktion ✓ 7. einmaleins ✓
8. multiplizieren-und-dividieren ✓ 9. dividieren-mit-rest ✓ 10. sachaufgaben ✓ 11. geld ✓ 12. laengen ✓ 13. gewichte ✓ 14. uhrzeit-und-zeitspannen ✓
15. koerper-und-figuren ✓ 16. achsensymmetrie ✓ 17. zahlenfolgen-und-muster ✓ 18. diagramme-und-tabellen ✓ 19. wahrscheinlichkeit ✓
DE / Mathe / Klasse 4（Zahlen bis 1 000 000）— 生成スクリプトは `gen_de_mathe_k4_*`（make_unit に grade="klasse-4"）。数詞は de_common.wort、6 桁の位取り表は stellentafel。
長さ・重さ・容量のコンマ表記（3,250 kg）の共通問題は `tools/de_k4_groessen.py`（komma・zwei・lesen・kleiner・groesser・rechnen）。Würfelnetz の折りたたみは K3 の roll・is_net を使う
1. zahlen-bis-1-million ✓ 2. runden-und-ueberschlagen ✓ 3. schriftlich-addieren-und-subtrahieren ✓ 4. schriftliche-multiplikation ✓ 5. schriftliche-division ✓ 6. rechengesetze-und-klammern ✓
7. brueche-im-alltag ✓ 8. sachaufgaben ✓ 9. laengen-mit-komma ✓ 10. gewichte-und-tonnen ✓ 11. rauminhalte ✓ 12. rechnen-mit-geld ✓ 13. zeit-und-kalender ✓ 14. massstab ✓
15. umfang-und-flaecheninhalt ✓ 16. parallel-senkrecht-und-vierecke ✓ 17. wuerfel-und-quader ✓ 18. daten-und-diagramme ✓ 19. kombinatorik-und-wahrscheinlichkeit ✓
DE / Mathe / Klasse 2（Zahlen bis 100。短い文、絵を多く）— 生成スクリプトは `gen_de_mathe_k2_*`（make_unit に grade="klasse-2"）。絵の部品は `tools/de_k2.py`（k_pics の絵にドイツ語の aria-label：hunderterfeld・punktfeld・gruppen・reihe・zahlenstrahl100、DING で物の名前）。
Flächen und Körper・Symmetrie・Diagramme は Klasse 3 の生成スクリプトの問題関数を、モジュールの R を新しい seed に入れ替えて再利用（Diagramme は 100 を超える数を le100 で落とす）
1. zahlen-bis-100 ✓ 2. zahlen-vergleichen-und-ordnen ✓ 3. plus-und-minus-bis-20 ✓ 4. plus-bis-100 ✓ 5. minus-bis-100 ✓ 6. ergaenzen-bis-100 ✓
7. multiplizieren-verstehen ✓ 8. einmaleins-mit-2-5-und-10 ✓ 9. kleines-einmaleins ✓ 10. geteilt-aufteilen-und-verteilen ✓ 11. sachaufgaben ✓ 12. geld ✓
13. laengen ✓ 14. uhrzeit ✓ 15. flaechen-und-koerper ✓ 16. spiegeln-und-symmetrie ✓ 17. zahlenmauern-und-muster ✓ 18. strichlisten-und-diagramme ✓
DE / Mathe / Klasse 1（Zahlen bis 20。とても短い文、ほぼ全問に絵）— 生成スクリプトは `gen_de_mathe_k1_*`（make_unit に grade="klasse-1"）。絵は k_pics（tenframe・dice・bond・box・two_groups・crossed_row・hop_line・pencils・towers・table_scene・box_scene・shelf など）を de_k2.de() でドイツ語の aria-label にして使う。
Formen・Formenmuster は Klasse 2 の生成スクリプトの問題関数を R を入れ替えて再利用。topic の正規表現に verdoppeln（plus-und-minus）・lage-und（geometrie）を足した
1. zahlen-bis-10 ✓ 2. zahlen-bis-20 ✓ 3. zahlen-vergleichen ✓ 4. zerlegen-und-ergaenzen ✓ 5. plus-bis-10 ✓ 6. minus-bis-10 ✓
7. plus-und-minus-bis-20 ✓ 8. plus-und-minus-ueber-die-10 ✓ 9. verdoppeln-und-halbieren ✓ 10. rechengeschichten-und-sachaufgaben ✓ 11. geld ✓
12. laengen-vergleichen-und-messen ✓ 13. uhrzeit-und-tagesablauf ✓ 14. formen-und-koerper ✓ 15. lage-und-richtung ✓ 16. muster-und-zahlenfolgen ✓ 17. strichlisten-und-tabellen ✓
DE / Mathe / Klasse 5（Sekundarstufe I。KMK-Bildungsstandards ESA/MSA 2022、de_common.STD_URL_SEK。make_unit は grade が klasse-5〜10 なら自動で Sek I の URL）— 生成スクリプトは `gen_de_mathe_k5_*`（make_unit に grade="klasse-5"）。
Leitidee に「F」Funktionaler Zusammenhang を足した。負の数を選択肢に入れるときは mcq(…, neg=True)。K3・K4 の問題関数（achsensymmetrie・umfang_und_flaecheninhalt・wuerfel_und_quader・daten_und_diagramme・brueche）を R を入れ替えて再利用。
zahlenstrahl は長いラベルに合わせて左右の余白を広げる。トピック: negative-zahlen・potenzen→zahlen、teiler・primzahl→mal-und-geteilt、strecken・koordinaten・winkel→geometrie、volumen→groessen
1. natuerliche-zahlen-und-stellenwerte ✓ 2. runden-und-schaetzen ✓ 3. negative-zahlen ✓ 4. addieren-und-subtrahieren ✓ 5. multiplizieren-und-dividieren ✓ 6. terme-und-rechengesetze ✓
7. potenzen-und-quadratzahlen ✓ 8. teiler-vielfache-und-primzahlen ✓ 9. brueche-und-anteile ✓ 10. laengen-massen-und-zeit ✓ 11. sachaufgaben-und-kombinatorik ✓ 12. strecken-geraden-und-strahlen ✓
13. koordinatensystem ✓ 14. winkel ✓ 15. achsen-und-punktsymmetrie ✓ 16. flaecheninhalt-und-umfang ✓ 17. volumen-und-oberflaeche-von-quadern ✓ 18. haeufigkeiten-und-diagramme ✓ 19. muster-terme-und-variablen ✓
DE / Mathe / Klasse 6（Sek I）— 生成スクリプトは `gen_de_mathe_k6_*`（make_unit に grade="klasse-6"）、共通部品は `tools/de_k6.py`（bh＝Fraction を HTML の分数に（gemischt=True で帯分数）、dz＝Fraction を正確な小数（コンマ）に、割り切れないときは ValueError、mcq＝誤答が足りないとき None を返して作り直し）。
お金は「%d,%02d €」で表示し、四捨五入は int(x * 100 + 1/2)（round() は偶数丸めになるので使わない）。循環小数は `<span class='ov'>3</span>`。トピック brueche-und-dezimalzahlen（Brüche, Dezimalzahlen und Prozente）を足した。zuordnung・gleichung→muster、kreis・dreieck→geometrie、negative→zahlen
1. brueche-erweitern-und-kuerzen ✓ 2. brueche-vergleichen-und-ordnen ✓ 3. gemischte-zahlen ✓ 4. brueche-addieren-und-subtrahieren ✓ 5. brueche-multiplizieren ✓ 6. brueche-dividieren ✓
7. dezimalzahlen-und-stellenwerte ✓ 8. brueche-und-dezimalzahlen ✓ 9. dezimalzahlen-addieren-und-subtrahieren ✓ 10. dezimalzahlen-multiplizieren-und-dividieren ✓ 11. prozente ✓ 12. rechnen-mit-negativen-zahlen ✓
13. zuordnungen-und-dreisatz ✓ 14. terme-und-gleichungen ✓ 15. kreise-und-kreisdiagramme ✓ 16. dreiecke-und-vierecke ✓ 17. flaecheninhalt-von-parallelogramm-und-dreieck ✓ 18. daten-und-wahrscheinlichkeit ✓
19. sachaufgaben-mit-bruechen-und-dezimalzahlen ✓
DE / Mathe / Klasse 7（Sek I）— 生成スクリプトは `gen_de_mathe_k7_*`（make_unit に grade="klasse-7"）、共通部品は `tools/de_k7.py`（de_k6 の上に mcq（neg=True）・rd（四捨五入）・eur（12,50 €、負は −）・pz（%）・zk）。
負の数は「−」、かっこ付きで（−3）。図はすべて `lg=True`（印刷で大きく。横長の viewBox にすると読みやすい）。トピック: rational→zahlen、zins→brueche-und-dezimalzahlen、terme→muster、prism→geometrie、boxplot→daten-und-zufall
1. rationale-zahlen ✓ 2. rechnen-mit-rationalen-zahlen ✓ 3. prozentrechnung ✓ 4. prozentuale-veraenderung ✓ 5. zinsrechnung ✓ 6. proportionale-und-antiproportionale-zuordnungen ✓
7. terme-umformen ✓ 8. lineare-gleichungen ✓ 9. gleichungen-in-sachaufgaben ✓ 10. winkel-an-geradenkreuzungen ✓ 11. winkelsummen-in-dreiecken-und-vielecken ✓ 12. dreiecke-konstruieren ✓
13. besondere-linien-im-dreieck ✓ 14. flaecheninhalt-von-vierecken ✓ 15. prismen ✓ 16. boxplots-und-kennwerte ✓ 17. wahrscheinlichkeit ✓
DE / Mathe / Klasse 8（Sek I）— 生成スクリプトは `gen_de_mathe_k8_*`（make_unit に grade="klasse-8"）、共通部品は `tools/de_k8.py`（de_k7 の上に expr（項の並び → 2x² − 3x + 5）・gl（y = mx + b）・par（負の数をかっこに）・kosy（座標平面の SVG。目盛りは偶数だけ大きく、lg））。
π は Taschenrechner の値で「auf eine Nachkommastelle」（末尾の 0 も表示）。Definitionsmenge は「D = ℚ ∖ {2}」。連立方程式は「I: …<br>II: …<br>」。トピック lineare-funktionen-und-gleichungssysteme を足した。wurzel→zahlen、ausmultipl・binomisch→muster（mal-und-geteilt の out に ausmultipl）、kongruenz・thales・zylinder→geometrie
1. potenzen-und-zehnerpotenzen ✓ 2. quadratwurzeln-und-reelle-zahlen ✓ 3. ausmultiplizieren-und-ausklammern ✓ 4. binomische-formeln ✓ 5. lineare-funktionen ✓ 6. geradengleichungen-aufstellen ✓
7. lineare-gleichungssysteme-grafisch-loesen ✓ 8. lineare-gleichungssysteme-rechnerisch-loesen ✓ 9. gleichungssysteme-in-sachaufgaben ✓ 10. kongruenzsaetze ✓ 11. satz-des-thales ✓
12. kreisumfang-und-kreisflaeche ✓ 13. zylinder ✓ 14. mehrstufige-zufallsexperimente ✓ 15. bruchterme-und-bruchgleichungen ✓
DE / Mathe / Klasse 9（Sek I）— 生成スクリプトは `gen_de_mathe_k9_*`（make_unit に grade="klasse-9"）、共通部品は `tools/de_k9.py`（de_k8 の上に zahl・zr（四捨五入した小数、末尾の 0 も表示）・qf（ax² + bx + c）・sform（y = a(x − d)² + e、かっこ内はノーブレークスペース）・parabel（放物線の SVG）・rdreieck（直角三角形の SVG、直角は C））。
長さ・お金の答えは分数でなく小数（割り切れないときは zr で丸める）。解の集合は「L = {−5; 3}」。トピック quadratische-funktionen-und-gleichungen を足した（lineare-funktionen-… の out に quadratisch）。potenz・wurzel→zahlen、pythagoras・aehnlich・strahlen・trigonometr・pyramide・kegel・kugel→geometrie、vierfelder→daten-und-zufall
1. potenzgesetze ✓ 2. rechnen-mit-wurzeln ✓ 3. quadratische-funktionen ✓ 4. scheitelpunktform-und-normalform ✓ 5. quadratische-gleichungen ✓ 6. quadratische-gleichungen-in-sachaufgaben ✓
7. satz-des-pythagoras ✓ 8. pythagoras-in-figuren-und-koerpern ✓ 9. aehnlichkeit-und-zentrische-streckung ✓ 10. strahlensaetze ✓ 11. trigonometrie ✓ 12. pyramide-und-kegel ✓ 13. kugel ✓ 14. vierfeldertafeln ✓
DE / Mathe / Klasse 10（Sek I の最後の学年）— 生成スクリプトは `gen_de_mathe_k10_*`（make_unit に grade="klasse-10"）、共通部品は `tools/de_k10.py`（de_k9 の上に pi_txt（π の倍数 → 「3π/2」）・kurve（任意の関数のグラフ。fs=[(f, 色, 名前)]、xr・yr=(lo, hi, 目盛り)、xlab で目盛りの文字を変える（π 単位）、lg））。
Bogenmaß は 180° = π。三角関数の値は「½√3」の形。電卓の答えは小数第 1〜2 位まで（「≈」）。トピック exponential-potenz-und-winkelfunktionen（Exponential-, Potenz- und Winkelfunktionen）を足した（lineare-funktionen-… の out に exponential|potenzfunktion|polynom|sinus、zahlen の out に potenzfunktion）。logarithm→zahlen、bogenmass・einheitskreis・sinussatz→geometrie、erwartungswert→daten-und-zufall
1. exponentialfunktionen ✓ 2. exponentielles-wachstum-und-zerfall ✓ 3. logarithmus ✓ 4. potenzfunktionen ✓ 5. polynomfunktionen ✓ 6. bogenmass-und-kreisausschnitt ✓
7. trigonometrie-am-einheitskreis ✓ 8. sinus-und-kosinusfunktion ✓ 9. sinussatz-und-kosinussatz ✓ 10. erwartungswert ✓
DE / Mathe は Klasse 1〜10 まで完了。次は GDP 順で次の国（日本は国内向けで別サイト。インドは下）

IN / Maths（CBSE 2025-26 / NCERT 教科書の章立て）— country `in`（name「India」、lang en、hreflang en-in）、subject `maths`、grade `class-N`（name「Class N」、N+5〜N+6 歳、unit.php）、A4。生成スクリプトは `gen_in_maths_cN_*`、共通部品は `tools/in_common.py`（sg_sec と同じ API。インドの数の書き方 1,23,456（lakh）・₹（inr）・インドの名前と地名、fv、adopt（他国の生成スクリプトの名前・お金・数をインド式に）、ok（LEAKS で $・GST・Singapore・miles など他国の語を落とす。4 桁以上の小数の選択肢も落とす）、collect は名前と代名詞を除いた問題文で重複を判定、make（CBSE の Unit と NCERT の章番号。q の先頭の図は qfig に入れて後ろへ、図は data-pf='lg'、ハイフンのマイナスを − に））。
1 単元 = NCERT の 1 章（章の名前を slug に）。standard_code は「Class 10, Chapter 4: Quadratic Equations」、domain は CBSE の Unit 名（Number Systems／Algebra／Coordinate Geometry／Geometry／Trigonometry／Mensuration／Statistics and Probability）、standard_text は CBSE シラバスの要約、standard_url は cbseacademic の Maths_Sec_2025-26.pdf。
イギリス式の綴り（colour, metre, factorisation, zeroes, maths）。π は 22/7（半径は 7 の倍数）、segment は π = 3.14・√3 = 1.73。三角比の値は 1/√2・√3/2 の形、高さと距離は 20√3 m の形。topic_gb() に in を入れた。topics.php の topic_defs() に $country === 'in' の調整（real-numbers→factors・exponents、progression→algebra、triangles→congruence-and-similarity、trigonometry・areas-related・surface-areas を shapes から外す）
SG Sec 2–3・US Geometry・AU Year 8 の問題関数を adopt で再利用（連立方程式、因数分解、二次方程式の文章題、相似、接線）

IN / Maths / Class 10（CBSE の board exam の学年）
1. real-numbers ✓ 2. polynomials ✓ 3. pair-of-linear-equations-in-two-variables ✓ 4. quadratic-equations ✓ 5. arithmetic-progressions ✓ 6. triangles ✓ 7. coordinate-geometry ✓
8. introduction-to-trigonometry ✓ 9. some-applications-of-trigonometry ✓ 10. circles ✓ 11. areas-related-to-circles ✓ 12. surface-areas-and-volumes ✓ 13. statistics ✓ 14. probability ✓

IN / Maths / Class 9（CBSE。NCERT の 12 章）— 生成スクリプトは `gen_in_maths_c9_*`。AU Year 8・US Algebra 1・Geometry・SG Sec 1・3 の問題関数を再利用（in_common.gb で米国式の綴り・m∠・CPCTC・HL→RHS などを直す）。
P を点の関数に使うモジュール（gen_sg_maths_s3_angle_properties_of_circles）は adopt しない。Statistics の CBSE Unit は「St」（UNITS）。LEAKS の "None" は「= None」などだけ（"None" という正しい答えを残す）。
度数折れ線の問題は 0 から始まる階級を使わない（仮の階級の階級値が負になるため）。topics.php の in の調整に number-systems→exponents-and-roots、heron→area-and-perimeter、euclid→angles を足した
1. number-systems ✓ 2. polynomials ✓ 3. coordinate-geometry ✓ 4. linear-equations-in-two-variables ✓ 5. introduction-to-euclids-geometry ✓ 6. lines-and-angles ✓
7. triangles ✓ 8. quadrilaterals ✓ 9. circles ✓ 10. herons-formula ✓ 11. surface-areas-and-volumes ✓ 12. statistics ✓

IN / Maths / Class 6–8（NCERT Ganita Prakash。1 単元 = 1 章。Class 7・8 は Part 1・2 に分かれ、章番号はパートごとに 1 から）— 生成スクリプトは `gen_in_maths_c6_*`・`c7_*`・`c8_*`。
in_common.unit(level, part, chapter, slug, sort, strand, …, spec, R) で作る（part=0 は Class 6、spec は [(セット名, [(maker, 数)])] × 5）。standard_code は「Class 8, Ganita Prakash Part 2, Chapter 1: …」、standard_url は STD_URL_MID（NCERT textbook）、domain は strand N/A/G/M/D（Number／Algebra／Geometry／Mensuration／Data Handling）。sort は Part 1 → Part 2 の通し番号。
unit() は全 maker を mid_ok で包む（MID_LEAKS で surf・backyard・sweets など他国の語を落とす、正解と同じ値の未約分の誤答（5/40 と 1/8）を落とす、a octagon → an octagon）。£ を書く UK の maker は in_common.rs()（£→₹、p→paise）。
UK KS3・AU Year 7–8・SG Sec 1–2・US Geometry、IN Class 9 の statistics（one_bar・one_hist・K）・triangles（ind）、Class 8 number play（one_crypt）、Class 6 prime time（one_common・one_prob）を再利用。topics.php の in の調整に Ganita Prakash の章名（$gp）を足した
Class 6: 1. patterns-in-mathematics ✓ 2. lines-and-angles ✓ 3. number-play ✓ 4. data-handling-and-presentation ✓ 5. prime-time ✓ 6. perimeter-and-area ✓ 7. fractions ✓ 8. playing-with-constructions ✓ 9. symmetry ✓ 10. the-other-side-of-zero ✓
Class 7 Part 1: 1. large-numbers-around-us ✓ 2. arithmetic-expressions ✓ 3. a-peek-beyond-the-point ✓ 4. expressions-using-letter-numbers ✓ 5. parallel-and-intersecting-lines ✓ 6. number-play ✓ 7. a-tale-of-three-intersecting-lines ✓ 8. working-with-fractions ✓
Class 7 Part 2: 1. geometric-twins ✓ 2. operations-with-integers ✓ 3. finding-common-ground ✓ 4. another-peek-beyond-the-point ✓ 5. connecting-the-dots ✓ 6. constructions-and-tilings ✓ 7. finding-the-unknown ✓
Class 8 Part 1: 1. a-square-and-a-cube ✓ 2. power-play ✓ 3. a-story-of-numbers ✓ 4. quadrilaterals ✓ 5. number-play ✓ 6. we-distribute-yet-things-multiply ✓ 7. proportional-reasoning-1 ✓
Class 8 Part 2: 1. fractions-in-disguise ✓ 2. the-baudhayana-pythagoras-theorem ✓ 3. proportional-reasoning-2 ✓ 4. exploring-some-geometric-themes ✓ 5. tales-by-dots-and-lines ✓ 6. algebra-play ✓ 7. area ✓

IN / Maths / Class 1–5（NCERT Joyful Mathematics（Class 1–2）・Maths Mela（Class 3–5）。1 単元 = 1 章）— 生成スクリプトは `gen_in_maths_c1_*`〜`c5_*`、共通部品は `tools/in_prim.py`（ph_common をインド向けにしたもの：インドの名前・地名、us_text（GB_WORDS）でイギリス式の綴り・$/£→₹・cuboid・L と mL・mixed number・Terry Fox Run などの言い換え、in_ok は LEAKS を SVG の文字・aria-label にも使う、collect・run_many・build_sets・finish）とお金の絵 `tools/in_money.py`（1〜20 ルピー硬貨、10〜500 ルピー札。one_name・one_count・one_cmp・one_buy・one_make(lim)）。
in_prim.unit(level, slug, sort, strand, chapter, …, specs, seed, max_num) で作る。specs の部品は `rn(mod("他国の生成スクリプト", seed), "set_x", 数, keep)`（引数を名前から自動で埋める。spots などは rn(..., spots=…) で渡す）と `co(maker, 数)`、数の問題は `num_maker(lo, hi, kinds)`。standard_code は「Class 5, Maths Mela Chapter 9: Coconut Farm」、domain は strand N/G/M/P/D（Numbers and Operations／Shapes and Space／Measurement／Patterns／Data Handling）、standard_url は NCERT textbook。seed は 60N0c（Class N の c 章）。
Class 1–2 は数にカンマなし、Class 3 から 1,000（インド式 1,00,000）。topics.php の in の調整に Class 1–5 の章名（$jm）を足した
Class 1: 1. finding-the-furry-cat ✓ 2. what-is-long-what-is-round ✓ 3. mango-treat ✓ 4. making-10 ✓ 5. how-many ✓ 6. vegetable-farm ✓ 7. linas-family ✓ 8. fun-with-numbers ✓ 9. utsav ✓ 10. how-do-i-spend-my-day ✓ 11. how-many-times ✓ 12. how-much-can-we-spend ✓ 13. so-many-toys ✓
Class 2: 1. a-day-at-the-beach ✓ 2. shapes-around-us ✓ 3. fun-with-numbers ✓ 4. shadow-story ✓ 5. playing-with-lines ✓ 6. decoration-for-festival ✓ 7. ranis-gift ✓ 8. grouping-and-sharing ✓ 9. which-season-is-it ✓ 10. fun-at-the-fair ✓ 11. data-handling ✓
Class 3: 1. whats-in-a-name ✓ 2. toy-joy ✓ 3. double-century ✓ 4. vacation-with-my-nani-maa ✓ 5. fun-with-shapes ✓ 6. house-of-hundreds-1 ✓ 7. raksha-bandhan ✓ 8. fair-share ✓ 9. house-of-hundreds-2 ✓ 10. fun-at-class-party ✓ 11. filling-and-lifting ✓ 12. give-and-take ✓ 13. time-goes-on ✓ 14. the-surajkund-fair ✓
Class 4: 1. shapes-around-us ✓ 2. hide-and-seek ✓ 3. pattern-around-us ✓ 4. thousands-around-us ✓ 5. sharing-and-measuring ✓ 6. measuring-length ✓ 7. the-cleanest-village ✓ 8. weigh-it-pour-it ✓ 9. equal-groups ✓ 10. elephants-tigers-and-leopards ✓ 11. fun-with-symmetry ✓ 12. ticking-clocks-and-turning-calendar ✓ 13. the-transport-museum ✓ 14. data-handling ✓
Class 5: 1. we-the-travellers-1 ✓ 2. fractions ✓ 3. angles-as-turns ✓ 4. we-the-travellers-2 ✓ 5. far-and-near ✓ 6. the-dairy-farm ✓ 7. shapes-and-patterns ✓ 8. weight-and-capacity ✓ 9. coconut-farm ✓ 10. symmetrical-designs ✓ 11. grandmothers-quilt ✓ 12. racing-seconds ✓ 13. animal-jumps ✓ 14. maps-and-locations ✓ 15. data-through-pictures ✓

IN / Maths / Class 11–12（CBSE Senior Secondary 2025-26 / NCERT。1 単元 = 1 章、Class 12 の章番号は Part I・II の通し番号）— 生成スクリプトは `gen_in_maths_c11_*`・`gen_in_maths_c12_*`、共通部品は `tools/in_sr.py`（in_common の上に U()（in_common.unit を level 11・12、part なしで呼ぶ。全 maker を tidy で包み「− −2」→「+ 2」「+ −3」→「− 3」）、use(mod, name, R, pairs)（adopt＋gb＋文字の置き換え。pairs に正規表現も可）、T2（誤答の重複を除く）、poly・xp・sup・pi（π の倍数）・surd・rt（√ の簡約）・frs、ⁿCᵣ の C()・P()、US の <sub>n</sub>C を ⁿC にする NCR）。
standard_code は「Class 12, Chapter 7: Integrals」、standard_url は CBSE SrSec の Maths_SrSec_2025-26.pdf（in_common.STD_URL_SR、level ≥ 11 で自動）、domain は CBSE の Unit（SF Sets and Functions／II Algebra／III Coordinate Geometry／Ca Calculus／VII Statistics and Probability／RF Relations and Functions／V3 Vectors and Three-Dimensional Geometry／LP Linear Programming／Pr Probability）。seed は 9111cc・9121cc。
US Algebra 2・Precalculus・Geometry、TX Algebra II・Precalculus、SG Sec 3–4 の問題関数を use() で再利用（Quadrant II→the second quadrant、ft の問題は落とす）、微積分・ベクトル（î ĵ k̂）・3D・LPP・微分方程式は自前。行列は pc_common.mat／det_h。NCERT の log は自然対数。topics.php の in の調整に calculus（名前を Calculus に）・vectors-and-matrices・coordinates-and-position を足した
Class 11: 1. sets ✓ 2. relations-and-functions ✓ 3. trigonometric-functions ✓ 4. complex-numbers-and-quadratic-equations ✓ 5. linear-inequalities ✓ 6. permutations-and-combinations ✓ 7. binomial-theorem ✓ 8. sequences-and-series ✓ 9. straight-lines ✓ 10. conic-sections ✓ 11. introduction-to-three-dimensional-geometry ✓ 12. limits-and-derivatives ✓ 13. statistics ✓ 14. probability ✓
Class 12: 1. relations-and-functions ✓ 2. inverse-trigonometric-functions ✓ 3. matrices ✓ 4. determinants ✓ 5. continuity-and-differentiability ✓ 6. application-of-derivatives ✓ 7. integrals ✓ 8. application-of-integrals ✓ 9. differential-equations ✓ 10. vector-algebra ✓ 11. three-dimensional-geometry ✓ 12. linear-programming ✓ 13. probability ✓

IN / Maths は Class 1〜12 まで完了。次は GDP 順で次の国

FR / Maths（Programmes 2024 du cycle 2、BO n°41 du 31 octobre 2024、2025 年度から）— country `fr`（name「France」、lang `fr`、hreflang fr-fr）、subject `maths`（Maths）、grade `ce2`（name「CE2」、sort 3、8〜9歳。cp 1・ce1 2・ce2 3・cm1 4・cm2 5、unit.php に年齢あり）、A4。生成スクリプトは `gen_fr_maths_ce2_*`、共通部品は `tools/fr_common.py`（num・dec・eur（3,50 €・45 c）・hm（8 h 15）・dur（1 h 25 min）・fp（: ; ? ! の前にノーブレークスペース。mcq が q と e に自動で使う）・Kids（名前と il/elle）・mcq・mix・lesson（Comment faire → Exemple → Erreurs fréquentes）・make_unit・lettres（数詞）・図：droite・numeration・blocs・barres・argent_svg（€ の硬貨と札）・solide_svg・horloge・posee（筆算）・bande・disque・droite_frac（分数））。
フランス語、tu で話しかける短い文。記号は × と ÷。1 000 以上はノーブレークスペース区切り、小数はコンマ。アポストロフィは ’（まっすぐな ' は使わない）。「de」「que」「à le」の縮約に注意（d’élèves、qu’Ambre、au rond）。
short_title は冠詞なしで大文字始まり（「Fractions」「Addition posée」）。standard_code は「CE2 · Grandeurs et mesures」形式（domain は Nombres, calcul et résolution de problèmes／Grandeurs et mesures／Espace et géométrie／Organisation et gestion des données）、standard_text は要約、standard_url は BO 2024 n°41。
UI 文言は core.php の 'fr'（js の桁区切りはノーブレークスペース、'colon' で「 :」）。トピックは topics.php の `topic_defs_fr()`（nombres・addition-et-soustraction・multiplication-et-division・fractions・problemes・grandeurs-et-mesures・geometrie・donnees）。topic.php・topics.php に $fr の文言。preview.php の大文字は mb_strtoupper（pv_up）
symétrie・solides は DE Klasse 3 の生成スクリプトの関数（grid・mirror・wuerfelnetz・bauplan）を R を入れ替えて使い、文字をフランス語に置き換える

FR / Maths / CE2
1. nombres-jusqu-a-10-000 ✓ 2. comparer-et-ranger-les-nombres ✓ 3. calcul-mental ✓ 4. addition-posee ✓ 5. soustraction-posee ✓ 6. tables-de-multiplication ✓
7. multiplication-posee ✓ 8. division-et-partages ✓ 9. fractions ✓ 10. additionner-et-soustraire-des-fractions ✓ 11. problemes ✓ 12. longueurs-et-perimetres ✓
13. masses-et-contenances ✓ 14. heures-et-durees ✓ 15. monnaie ✓ 16. solides ✓ 17. figures-planes-et-angles-droits ✓ 18. symetrie-axiale ✓
19. se-reperer-et-se-deplacer ✓ 20. tableaux-et-diagrammes ✓

FR / Maths / CM1・CM2（Programmes 2025 du cycle 3、BO n°16 du 17 avril 2025。CM1 は 2025 年度、CM2 は 2026 年度から）— grade `cm1`（sort 4）・`cm2`（sort 5）。
生成スクリプトは `gen_fr_maths_cm1_*` に `build(lv)`（lv = 1 または 2）を書き、`gen_fr_maths_cm2_*` は `build(2)` を呼ぶだけ（seed は 52100 + 100 × lv + 番号）。共通部品は `tools/fr_c3.py`（fr_common の上に dz（整数 → コンマの小数）・lettres_big（999 999 999 までの数詞）・nomfrac（3/4 → trois quarts）・RANGS／RANGP・de（d’élèves）・droite_dec・unit（seo_title を自動、standard_text に「(résumé du programme 2025 du cycle 3)」））。
fr_common.make_unit は cm1・cm2 で standard_url を BO 2025（STD_URL_C3）にし、domain に「P」Proportionnalité と「D」Organisation et gestion de données et probabilités を使う。
範囲：CM1 は 999 999・小数 2 桁・分母 20 まで、CM2 は 999 999 999・小数 3 桁・分母 60 まで。CE2 の生成スクリプトの問題関数（時刻・グラフ・図形・立体・対称）を R を入れ替えて再利用。
set を作ってから list にするときは sorted() してから shuffle（文字列を含む set は実行ごとに順番が変わる）。トピックに nombres-decimaux と algebre-et-proportionnalite を足した
1. nombres（cm1: nombres-jusqu-a-999-999、cm2: nombres-jusqu-a-999-999-999）✓ 2. comparer-encadrer-et-ranger-les-nombres ✓ 3. multiples-et-diviseurs ✓ 4. calcul-mental ✓ 5. addition-et-soustraction-posees ✓
6. multiplication-posee ✓ 7. division（cm1: division-euclidienne、cm2: division-decimale）✓ 8. fractions ✓ 9. comparer-additionner-et-soustraire-des-fractions ✓
10. fraction-d-une-quantite（cm2: fraction-d-une-quantite-et-multiplication）✓ 11. fractions-decimales ✓ 12. nombres-decimaux ✓ 13. egalites-a-trous-et-programmes-de-calcul ✓ 14. problemes ✓
15. proportionnalite ✓ 16. longueurs-et-perimetres ✓ 17. masses-et-contenances ✓ 18. aires ✓ 19. angles ✓ 20. heures-et-durees ✓ 21. figures-planes ✓ 22. symetrie-axiale ✓
23. solides-et-patrons ✓ 24. tableaux-et-graphiques ✓ 25. probabilites ✓

FR / Maths / CP・CE1（Programmes 2024 du cycle 2、BO n°41。CE2 と同じルール）— grade `cp`（sort 1、6〜7歳）・`ce1`（sort 2）。
生成スクリプトは `gen_fr_maths_cp_*` に `build(lv)`（lv = 0 は CP、1 は CE1、seed は 53000 + 100 × lv + 番号）、`gen_fr_maths_ce1_*` は `build(1)` を呼ぶだけ（CE1 だけの 4 単元は自前）。共通部品は `tools/fr_c2.py`（fr_common の上に G・GN、CHOSE（k_pics の絵 → フランス語の名詞と性）、ch・nom・un・le・de、pic（k_pics の SVG にフランス語の aria-label）、pl（1 dizaine / 3 dizaines）、que・de_n（qu’Ambre・d’Ambre）、unit（seo_title を自動、standard_text に「(résumé du programme 2024 du cycle 2)」））。
範囲：CP は 100 まで（計算は 20 まで、2 桁の繰り上がり 1 回まで、お金は整数の €、時刻は heure pile）、CE1 は 999 まで（分数は 1 以下、時刻は quart・demie）。CP はほぼ全問に絵（k_pics・f_common.glasses_svg）。CE2 の生成スクリプトの問題関数（時刻・お金・図形・立体・対称・座標・データ・分数・九九）を R を入れ替えて再利用（CE1 の範囲外は包んで落とす：losange、2 unités、小数 × 整数など）。
トピック：compter→nombres、complements・doubles-et-moities→addition-et-soustraction、tables-d-addition は multiplication の out
CP: 1. nombres-jusqu-a-100 ✓ 2. comparer-et-ranger-les-nombres ✓ 3. compter-et-suites ✓ 4. tables-d-addition ✓ 5. calcul-mental ✓ 6. addition-posee ✓ 7. sens-de-la-soustraction ✓ 8. doubles-et-moities ✓ 9. problemes ✓
10. longueurs ✓ 11. masses-et-contenances ✓ 12. monnaie ✓ 13. lire-l-heure ✓ 14. figures-planes ✓ 15. solides ✓ 16. se-reperer-et-se-deplacer ✓ 17. tableaux-et-diagrammes ✓
CE1: 1. nombres-jusqu-a-1000 ✓ 2. comparer-et-ranger-les-nombres ✓ 3. compter-pair-et-impair ✓ 4. complements-a-la-dizaine-et-a-100 ✓ 5. calcul-mental ✓ 6. addition-posee ✓ 7. soustraction-posee ✓ 8. doubles-et-moities ✓ 9. problemes ✓
10. longueurs-et-perimetres ✓ 11. masses-et-contenances ✓ 12. monnaie ✓ 13. heures-et-durees ✓ 14. figures-planes-et-angles-droits ✓ 15. solides ✓ 16. se-reperer-et-se-deplacer ✓ 17. tableaux-et-diagrammes ✓
18. sens-de-la-multiplication ✓ 19. tables-de-multiplication ✓ 20. fractions ✓ 21. symetrie-axiale ✓

FR の次: 6e〜3e（collège、cycle 3 の 6e と cycle 4）。catalog.json に学年を足す

その後: …（新しい学年・国は `catalog.json` に追加）

## 日本語辞書（/japanese/{言語}/word/{単語}.html）— PHP + DB

- 単語ページは `site/japanese/_dict/word.php` が DB の **jd_word**（1語1行、13言語の訳を JSON）から作る。ルーティングは `site/japanese/.htaccess`
- 言語: en vi zh tw ko id es pt fr de ru th ar（13言語。単語ページは PHP なのでファイルは増えない）
- 正本は `jdict/words/*.json`（公開済みの全語・13言語）。外のフォルダには頼らない（作業環境が消えても作り直せる）
- 語を増やす: `jdict/todo/BATCH.json`（40語の一覧）→ キュー `jdict/queue.txt`（`tools/jdict_next.sh` で1つ取り出す）→
  書き手が `jdict/BRIEF.md` のとおり `jdict/batches/BATCH/`（base.json＋8言語）を作る → `python3 tools/jdict_check.py BATCH` でエラー0 →
  `python3 tools/build_jdict.py`（そろったバッチを取り込み、words・一覧ページ・index.json・サイトマップ・lastmod を作る。tw は zh から OpenCC）→ コミット・push
- `build_jdict.py` は新しい語がないとき公開済みのファイルを1文字も変えない（変わったら不具合）
- 反映: push で Actions が `site/japanese/` の変わったファイルだけを `/aplus/japanese/` へ put（mirror は使わない。単語の .html が多いため）、`tools/sync_jd.py` → `worksheets/api/jd_sync.php` が jd_word へ書く
- 公開済みの語の URL（slug）は build_jdict.py が jdict/words から読んで固定する。作成途中のバッチがあっても、いつでも公開してよい
- jd_word は追加・上書きだけ（INSERT … ON DUPLICATE KEY UPDATE）。DELETE・DROP・ALTER は書かない
- 移行中: サーバーに単語の .html が残っている間はそちらが優先。削除し終えたら `.htaccess` の `RewriteCond %{REQUEST_FILENAME} !-f` を消す

## 触ってはいけないもの

- `site/worksheets/inc/secret.php`（サーバーにだけある鍵。リポジトリに入れない）
- DB は ws_ で始まる4テーブルと jd_word 以外を変更しない（`api/sync.php` は ws_ の4つ、`api/jd_sync.php` は jd_word だけを書く）
- `/aplus/` の他のフォルダ、`/aplus/sitemap.php`（このリポジトリの外）
