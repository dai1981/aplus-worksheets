unit(fname="numbers_to_120", slug="numbers-to-120", sort=1, domain=NO, code="1.2B, 1.2C", seed=69101,
  title="Numbers to 120: Tens and Ones", short="Numbers to 120",
  doc="Base-ten blocks, teen numbers, tens and ones in a number, tens with 0 ones and more than 9 ones, and stories\n(the US Grade 1 makers with Texas names).\nWrong answers come from real mistakes: swapping the tens and the ones, counting a rod as 1, and writing 40 + 5 as 405.",
  imports=mods(("gen_us_math_g1_place_value", "pv")) + "\nimport random\npv.P = pv.People(random.Random(69101))",
  specs='''        ("Count tens and ones in blocks", [("run", pv.set_blocks, ("rnd", "seen"), 20)]),
        ("Teen numbers: 1 ten and some ones", [("run", pv.set_teens, ("rnd", "seen"), 20)]),
        ("Tens and ones in a number", [("run", pv.set_digits, ("rnd", "seen"), 20)]),
        ("Tens with 0 ones, and more than 9 ones", [("run", pv.set_decades, ("rnd", "seen"), 20)]),
        ("Tens and ones stories", [("run", pv.set_story, ("rnd", "seen"), 20)]),''',
  think="<ul><li>A <b>ten</b> is 10 ones put together. A rod shows 1 ten.</li><li>In 47, the 4 means 4 tens (40) and the 7 means 7 ones.</li><li>47 = 40 + 7. This is the <b>expanded form</b>.</li><li>12 ones is the same as 1 ten and 2 ones.</li></ul>",
  examples='example("3 rods and 6 cubes", ["3 tens = 30", "30 + 6"], "36")',
  mistakes=[["Swapping tens and ones", "The tens digit is on the left."], ["Counting a rod as 1", "Each rod is 10."], ["Writing 40 + 5 as 405", "40 + 5 = 45."]],
  faq=[("What does TEKS 1.2B ask?", "Use concrete and pictorial models to compose and decompose numbers up to 120 in more than one way as so many hundreds, so many tens, and so many ones."), ("What does TEKS 1.2C ask?", "Use objects, pictures, and expanded and standard forms to represent numbers up to 120."), ("Is 1 ten and 14 ones the same as 24?", "Yes. 10 + 14 = 24."), ("What is expanded form?", "A number written as tens plus ones, like 30 + 6.")],
  std="1.2B use concrete and pictorial models to compose and decompose numbers up to 120 in more than one way as so many hundreds, so many tens, and so many ones; 1.2C use objects, pictures, and expanded and standard forms to represent numbers up to 120",
  meta="Free Grade 1 place value worksheets for Texas TEKS 1.2B and 1.2C: base-ten blocks, teen numbers, tens and ones and expanded form to 120. 100 questions with answers.",
  kb="A ten is 10 ones. 47 is 4 tens and 7 ones.", ks="47 = 40 + 7", seo="Grade 1 Numbers to 120: Tens and Ones Worksheets (TEKS 1.2B)")

unit(fname="compare_numbers", slug="comparing-and-ordering-numbers", sort=2, domain=NO, code="1.2D, 1.2E, 1.2F, 1.2G", seed=69102,
  title="Comparing and Ordering Numbers to 120", short="Comparing and Ordering Numbers",
  doc="Comparing tens first, then ones, the symbols >, < and =, greatest, least and in order, comparing with blocks, and\nword problems (the US Grade 1 makers with Texas names).\nWrong answers come from real mistakes: comparing the ones first, turning the symbol the wrong way, and reading 52 as 25.",
  imports=mods(("gen_us_math_g1_compare", "cm")),
  specs='''        ("Compare with tens and ones blocks", [("run", cm.set_blocks, ("rnd", "seen"), 20)]),
        ("Compare the tens first, then the ones", [("run", cm.set_places, ("rnd", "seen"), 20)]),
        ("Use the symbols >, < and =", [("run", cm.set_symbols, ("rnd", "seen"), 20)]),
        ("Greatest, least and in order", [("run", cm.set_order, ("rnd", "seen"), 20)]),
        ("Word problems", [("run", cm.set_words, ("rnd", "seen", cm.People), 20)]),''',
  think="<ul><li>Compare the <b>tens</b> first. More tens means a greater number.</li><li>If the tens are the same, compare the <b>ones</b>.</li><li>&gt; means greater than, &lt; means less than, = means equal to. The open side faces the greater number.</li><li>To order numbers, find the least, then the next, and so on.</li></ul>",
  examples='example("Compare 43 and 61", ["4 tens &lt; 6 tens"], "43 &lt; 61")',
  mistakes=[["Comparing the ones first", "Look at the tens first."], ["Turning the symbol the wrong way", "The open side faces the greater number."], ["Reading 52 as 25", "Say the tens digit first."]],
  faq=[("What does TEKS 1.2E ask?", "Use place value to compare whole numbers up to 120 using comparative language."), ("What does TEKS 1.2G ask?", "Represent the comparison of two numbers to 100 using the symbols &gt;, &lt;, or =."), ("What does TEKS 1.2F ask?", "Order whole numbers up to 120 using place value and open number lines."), ("What does TEKS 1.2D ask?", "Generate a number that is greater than or less than a given whole number up to 120.")],
  std="1.2D generate a number that is greater than or less than a given whole number up to 120; 1.2E use place value to compare whole numbers up to 120 using comparative language; 1.2F order whole numbers up to 120 using place value and open number lines; 1.2G represent the comparison of two numbers to 100 using the symbols >, <, or =",
  meta="Free Grade 1 worksheets for Texas TEKS 1.2D–1.2G: compare numbers to 120 with blocks and place value, use >, < and =, and order numbers. 100 questions with answers.",
  kb="Compare the tens first, then the ones.", ks="43 &lt; 61 because 4 tens &lt; 6 tens.", seo="Grade 1 Comparing and Ordering Numbers Worksheets (TEKS 1.2E)")

unit(fname="facts", slug="addition-and-subtraction-facts-to-20", sort=5, domain=NO, code="1.3D", seed=69105,
  title="Addition and Subtraction Facts to 20", short="Facts to 20",
  doc="Adding and subtracting within 10, doubles and near doubles, making 10, and subtracting within 20 (the US Grade 1\nmakers with Texas names).\nWrong answers come from real mistakes: counting the start number again, adding instead of taking away, and being off by 1.",
  imports=mods(("gen_us_math_g1_add_sub_20", "fs")),
  specs='''        ("Add within 10", [("run", fs.set_add10, (fs.People,), 20)]),
        ("Subtract within 10", [("run", fs.set_sub10, (fs.People,), 20)]),
        ("Doubles and near doubles", [("run", fs.set_doubles, (fs.People,), 20)]),
        ("Make 10 to add", [("run", fs.set_make10, (fs.People,), 20)]),
        ("Subtract within 20 and word problems", [("run", fs.set_sub20, (fs.People,), 20)]),''',
  think="<ul><li><b>Count on</b> from the bigger number to add.</li><li><b>Doubles</b>: 6 + 6 = 12, so 6 + 7 is 1 more: 13.</li><li><b>Make 10</b>: 9 + 5 = 9 + 1 + 4 = 10 + 4 = 14.</li><li>To subtract, take away or think of addition: 13 − 4 = 9 because 9 + 4 = 13.</li></ul>",
  examples='example("8 + 5", ["8 + 2 = 10", "10 + 3"], "13")',
  mistakes=[["Counting the start number again", "Start counting at the next number."], ["Adding instead of taking away", "Look at the sign: − means take away."], ["Being off by 1", "Check with a related fact."]],
  faq=[("What does TEKS 1.3D ask?", "Apply basic fact strategies to add and subtract within 20, including making 10 and decomposing a number leading to a 10."), ("What is a near double?", "A fact like 6 + 7, which is 1 more than the double 6 + 6."), ("How does making 10 help?", "Adding to 10 first is easy: 8 + 5 = 8 + 2 + 3 = 13."), ("How can addition help subtraction?", "13 − 4 = ? Think 4 + ? = 13.")],
  std="1.3D apply basic fact strategies to add and subtract within 20, including making 10 and decomposing a number leading to a 10",
  meta="Free Grade 1 addition and subtraction facts worksheets for Texas TEKS 1.3D: add and subtract within 10 and 20, doubles, near doubles and making 10. 100 questions with answers.",
  kb="Count on, use doubles, or make 10.", ks="9 + 5 = 10 + 4 = 14", seo="Grade 1 Addition and Subtraction Facts to 20 Worksheets (TEKS 1.3D)")

unit(fname="strategies", slug="addition-and-subtraction-strategies", sort=6, domain=NO, code="1.3E", seed=69106,
  title="Addition and Subtraction Strategies", short="Addition and Subtraction Strategies",
  doc="Counting on and back, turn-around facts, subtracting by thinking addition, fact families, and choosing a strategy for\nword problems (the US Grade 1 makers with Texas names).\nWrong answers come from real mistakes: counting the start number, thinking 9 − 3 = 3 − 9, and mixing up the parts and the whole.",
  imports=mods(("gen_us_math_g1_strategies", "st")),
  specs='''        ("Count on and count back", [("run", st.set_count, (st.People,), 20)]),
        ("Turn-around facts and make a ten", [("run", st.set_turn_around, (st.People,), 20)]),
        ("Subtract by thinking addition", [("run", st.set_think_add, (st.People,), 20)]),
        ("Fact families", [("run", st.set_families, (st.People,), 20)]),
        ("Word problems: choose a strategy", [("run", st.set_stories, (st.People,), 20)]),''',
  think="<ul><li><b>Count on</b> to add small numbers; <b>count back</b> to take away small numbers.</li><li><b>Turn-around facts</b>: 2 + 5 = 5 + 2.</li><li><b>Think addition</b>: 12 − 5 = ? because 5 + 7 = 12.</li><li>A <b>fact family</b> uses the same 3 numbers: 3 + 4 = 7, 4 + 3 = 7, 7 − 3 = 4, 7 − 4 = 3.</li></ul>",
  examples='example("12 − 5", ["Think: 5 + ? = 12"], "7")',
  mistakes=[["Counting the start number", "Count on from the next number."], ["Turning around a subtraction", "9 − 3 is not 3 − 9."], ["Mixing up parts and whole", "The whole is the biggest number in a fact family."]],
  faq=[("What does TEKS 1.3E ask?", "Explain strategies used to solve addition and subtraction problems up to 20 using spoken words, objects, pictorial models, and number sentences."), ("What is a fact family?", "Facts that use the same three numbers."), ("Does the order matter in addition?", "No. 2 + 5 and 5 + 2 are both 7."), ("Does the order matter in subtraction?", "Yes. Start with the whole.")],
  std="1.3E explain strategies used to solve addition and subtraction problems up to 20 using spoken words, objects, pictorial models, and number sentences",
  meta="Free Grade 1 strategy worksheets for Texas TEKS 1.3E: count on and back, turn-around facts, think addition to subtract and fact families. 100 questions with answers.",
  kb="Count on, turn it around, or think addition.", ks="12 − 5 = 7 because 5 + 7 = 12.", seo="Grade 1 Addition and Subtraction Strategies Worksheets (TEKS 1.3E)")

unit(fname="word_problems", slug="word-problems-within-20", sort=7, domain=NO, code="1.3B, 1.3F, 1.5D", seed=69107,
  title="Addition and Subtraction Word Problems within 20", short="Word Problems within 20",
  doc="Joining and separating, parts and whole, comparing, unknowns in any position, and mixed problems (the US Grade 1\nmakers with Texas names).\nWrong answers come from real mistakes: adding when the story takes away, adding the two numbers in a compare story,\nand answering with a number from the story.",
  imports=mods(("gen_us_math_g1_word_problems", "wp")),
  specs='''        ("Join and separate", [("run", wp.set_result, ("rnd", wp.People, lambda r: wp.Ctx(r, wp.JOIN)), 20)]),
        ("Parts and whole", [("run", wp.set_parts, ("rnd", wp.People, lambda r: wp.Ctx(r, wp.PARTS)), 20)]),
        ("Compare: how many more, how many fewer", [("run", wp.set_compare, ("rnd", wp.People, lambda r: wp.Ctx(r, wp.CMP)), 20)]),
        ("Find the missing number", [("run", wp.set_unknown, ("rnd", wp.People, lambda r: wp.Ctx(r, wp.JOIN)), 20)]),
        ("Mixed word problems", [("run", wp.set_mixed, ("rnd", wp.People, lambda r: wp.Ctx(r, wp.JOIN), lambda r: wp.Ctx(r, wp.PARTS), lambda r: wp.Ctx(r, wp.CMP)), 20)]),''',
  think="<ul><li>Read the story. Is something <b>joined</b>, <b>taken away</b>, or <b>compared</b>?</li><li>Join: add. Take away: subtract. How many more: subtract.</li><li>Write a number sentence with a box for the unknown: 7 + ☐ = 12.</li><li>Check: does the answer make sense in the story?</li></ul>",
  examples='example("Ava has 7 shells. She finds some more. Now she has 12.", ["7 + ☐ = 12"], "5 shells")',
  mistakes=[["Adding when the story takes away", "Look for words like gave away or ate."], ["Adding in a compare story", "How many more means subtract."], ["Answering with a number from the story", "Find the unknown."]],
  faq=[("What does TEKS 1.3B ask?", "Use objects and pictorial models to solve word problems involving joining, separating, and comparing sets within 20 and unknowns as any one of the terms in the problem such as 2 + 4 = [ ]; 3 + [ ] = 7; and 5 = [ ] − 3."), ("What does TEKS 1.3F ask?", "Generate and solve problem situations when given a number sentence involving addition or subtraction of numbers within 20."), ("What does TEKS 1.5D ask?", "Represent word problems involving addition and subtraction of whole numbers up to 20 using concrete and pictorial models and number sentences."), ("What is an unknown?", "The number the story does not tell you.")],
  std="1.3B use objects and pictorial models to solve word problems involving joining, separating, and comparing sets within 20 and unknowns as any one of the terms in the problem; 1.3F generate and solve problem situations when given a number sentence involving addition or subtraction of numbers within 20; 1.5D represent word problems involving addition and subtraction of whole numbers up to 20 using concrete and pictorial models and number sentences",
  meta="Free Grade 1 word problem worksheets for Texas TEKS 1.3B, 1.3F and 1.5D: join, separate, compare and missing number stories within 20. 100 questions with answers.",
  kb="Join: add. Take away or compare: subtract.", ks="7 + ☐ = 12, so ☐ = 5.", seo="Grade 1 Word Problems within 20 Worksheets (TEKS 1.3B)")

unit(fname="counting", slug="counting-to-120", sort=9, domain=AR, code="1.5A", seed=69109,
  title="Counting Forward and Backward to 120", short="Counting to 120",
  doc="What comes next or before, missing numbers on a 120 chart, counting objects, reading number words, and counting\npast 100 (the US Grade 1 makers with Texas names).\nWrong answers come from real mistakes: skipping a decade change (59, 50), writing 100 and 1 as 1001, and counting\nthe wrong way.",
  imports=mods(("gen_us_math_g1_count_120", "cn")),
  specs='''        ("Count objects", [("run", cn.set_objects, ("rnd", cn.People), 20)]),
        ("What comes next or before", [("run", cn.set_next, ("rnd", cn.People), 20)]),
        ("Read and write numbers", [("run", cn.set_words, ("rnd", cn.People), 20)]),
        ("Missing numbers on a 120 chart", [("run", cn.set_chart, ("rnd", cn.People), 20)]),
        ("Count past 100 and stories", [("run", cn.set_stories, ("rnd", cn.People), 20)]),''',
  think="<ul><li>Count <b>forward</b>: each number is 1 more. Count <b>backward</b>: each number is 1 less.</li><li>After 59 comes 60: the ones go back to 0 and the tens go up.</li><li>After 100 comes 101, 102, … 120.</li><li>On a 120 chart, the number to the right is 1 more.</li></ul>",
  examples='example("98, 99, 100, ☐", ["1 more than 100"], "101")',
  mistakes=[["Missing the decade change", "After 59 comes 60."], ["Writing 101 as 1001", "One hundred one is 101."], ["Counting the wrong way", "Backward means 1 less each time."]],
  faq=[("What does TEKS 1.5A ask?", "Recite numbers forward and backward from any given number between 1 and 120."), ("What comes after 109?", "110."), ("What comes before 100?", "99."), ("How can a 120 chart help?", "Move right for 1 more and down for 10 more.")],
  std="1.5A recite numbers forward and backward from any given number between 1 and 120",
  meta="Free Grade 1 counting worksheets for Texas TEKS 1.5A: count forward and backward to 120, next and before, number words and 120 chart puzzles. 100 questions with answers.",
  kb="Forward is 1 more; backward is 1 less.", ks="59, 60, 61 … 99, 100, 101", seo="Grade 1 Counting to 120 Worksheets (TEKS 1.5A)")

unit(fname="skip_counting", slug="skip-counting-by-2s-5s-and-10s", sort=10, domain=AR, code="1.5B", seed=69110,
  title="Skip Counting by 2s, 5s and 10s", short="Skip Counting",
  doc="Counting pairs by 2s, hands by 5s, bundles by 10s, patterns and missing numbers, and counting collections in groups\n(the Australian Year 1 makers with Texas names; coin items are left out).\nWrong answers come from real mistakes: counting each group as 1, counting by the wrong number, and stopping one\ngroup early.",
  imports=mods(("gen_au_maths_y1_skip_counting", "sk")),
  extra=UNIQ + ABCD + '''
set_stories = abcd(sk, sk.set_stories, 691101)


def skip(step):
    def f(r):
        start = step * r.randint(1, 110 // step)
        seq = [start + step * i for i in range(4)]
        nxt = seq[-1] + step
        if nxt > 120:
            raise AssertionError
        w = [seq[-1] + 1, seq[-1] + 2 * step, seq[-1] + (5 if step != 5 else 2)]
        return mcq("Count by %ds: %s, ☐. What comes next?" % (step, ", ".join(map(str, seq))), str(nxt), [str(x) for x in w],
                   "Add %d each time: %d + %d = <b>%d</b>." % (step, seq[-1], step, nxt))
    f.__name__ = "skip%d" % step
    return f


one_by5 = skip(5)
one_by10 = skip(10)


def no_coin(it):
    t = it["q"] + " ".join(it["c"]) + it["e"]
    return "coin" not in t and "c " not in t
''',
  specs='''        ("Count pairs by 2s", [("run", sk.set_twos, (sk.People,), 20, no_coin)]),
        ("Count hands by 5s", [("run", sk.set_fives, (sk.People,), 15, no_coin), ("collect", uniq(one_by5), 5)]),
        ("Count bundles by 10s", [("run", sk.set_tens, (sk.People,), 15, no_coin), ("collect", uniq(one_by10), 5)]),
        ("Continue the pattern", [("run", sk.set_patterns, (sk.People,), 20, no_coin)]),
        ("Count a collection in groups", [("run", set_stories, (sk.People,), 20, no_coin)]),''',
  think="<ul><li>Skip counting is a fast way to count groups.</li><li>By 2s: 2, 4, 6, 8, 10.</li><li>By 5s: 5, 10, 15, 20, 25.</li><li>By 10s: 10, 20, 30, 40, 50.</li><li>Say one number for each group.</li></ul>",
  examples='example("4 hands", ["5, 10, 15, 20"], "20 fingers")',
  mistakes=[["Counting each group as 1", "Each hand is 5, not 1."], ["Counting by the wrong number", "Pairs go by 2s, hands by 5s."], ["Stopping one group early", "Touch each group as you count."]],
  faq=[("What does TEKS 1.5B ask?", "Skip count by twos, fives, and tens to determine the total number of objects up to 120 in a set."), ("Why skip count?", "It is faster than counting by 1s."), ("What comes after 35 when counting by 5s?", "40."), ("What comes after 70 when counting by 10s?", "80.")],
  std="1.5B skip count by twos, fives, and tens to determine the total number of objects up to 120 in a set",
  meta="Free Grade 1 skip counting worksheets for Texas TEKS 1.5B: count by 2s, 5s and 10s with pictures, patterns and stories. 100 questions with answers.",
  kb="Say one number for each group.", ks="2, 4, 6 · 5, 10, 15 · 10, 20, 30", seo="Grade 1 Skip Counting by 2s, 5s and 10s Worksheets (TEKS 1.5B)")

unit(fname="ten_more_less", slug="10-more-and-10-less", sort=11, domain=AR, code="1.5C", seed=69111,
  title="10 More and 10 Less", short="10 More and 10 Less",
  doc="10 more and 10 less with base-ten blocks, on a hundred chart, mixed with 1 more and 1 less, and stories (the US\nGrade 1 makers with Texas names).\nWrong answers come from real mistakes: changing the ones digit, adding 1 instead of 10, and going the wrong way.",
  imports=mods(("gen_us_math_g1_ten_more_less", "tm")),
  specs='''        ("10 more with base-ten blocks", [("run", tm.set_more_blocks, ("rnd",), 20)]),
        ("10 less with base-ten blocks", [("run", tm.set_less_blocks, ("rnd",), 20)]),
        ("Use a hundred chart", [("run", tm.set_chart, ("rnd",), 20)]),
        ("10 more, 10 less, 1 more, 1 less", [("run", tm.set_mixed, ("rnd",), 20)]),
        ("Word problems: 10 more and 10 less", [("run", tm.set_stories, ("rnd", tm.People), 20)]),''',
  think="<ul><li><b>10 more</b>: the tens digit goes up by 1. 34 → 44.</li><li><b>10 less</b>: the tens digit goes down by 1. 34 → 24.</li><li>The ones digit stays the same.</li><li>On a hundred chart, 10 more is the number just below.</li></ul>",
  examples='example("10 more than 38", ["3 tens → 4 tens"], "48")',
  mistakes=[["Changing the ones digit", "Only the tens change."], ["Adding 1 instead of 10", "10 more than 38 is 48, not 39."], ["Going the wrong way", "More goes up; less goes down."]],
  faq=[("What does TEKS 1.5C ask?", "Use relationships to determine the number that is 10 more and 10 less than a given number up to 120."), ("What is 10 more than 95?", "105."), ("What is 10 less than 110?", "100."), ("Why does only the tens digit change?", "Adding or taking 1 ten does not change the ones.")],
  std="1.5C use relationships to determine the number that is 10 more and 10 less than a given number up to 120",
  meta="Free Grade 1 worksheets for Texas TEKS 1.5C: find 10 more and 10 less with blocks, a hundred chart and stories. 100 questions with answers.",
  kb="Only the tens digit changes.", ks="10 more than 38 is 48; 10 less is 28.", seo="Grade 1 10 More and 10 Less Worksheets (TEKS 1.5C)")

unit(fname="equal_sign", slug="equal-sign-and-missing-numbers", sort=12, domain=AR, code="1.5E, 1.5F", seed=69112,
  title="The Equal Sign and Missing Numbers", short="Equal Sign and Missing Numbers",
  doc="What the equal sign means, true or false number sentences, missing numbers on either side, and stories (the US\nGrade 1 makers with Texas names).\nWrong answers come from real mistakes: thinking = means the answer comes next, adding all the numbers, and\nreading 8 = 3 + 5 as false.",
  imports=mods(("gen_us_math_g1_equal_sign", "eq")),
  specs='''        ("“=” means “the same as”", [("run", eq.set_same_as, (eq.People,), 20)]),
        ("True or false?", [("run", eq.set_true_false, (eq.People,), 20)]),
        ("Find the missing number", [("run", eq.set_right_middle, (eq.People,), 20)]),
        ("Missing number on either side", [("run", eq.set_left_both, (eq.People,), 20)]),
        ("Word problems with a missing number", [("run", eq.set_stories, (eq.People,), 20)]),''',
  think="<ul><li>The <b>equal sign</b> means both sides have the <b>same value</b>.</li><li>8 = 3 + 5 is true. 4 + 4 = 3 + 5 is true too.</li><li>To find a missing number, make both sides the same: 6 + ☐ = 10, so ☐ = 4.</li></ul>",
  examples='example("4 + ☐ = 3 + 6", ["3 + 6 = 9", "4 + 5 = 9"], "5")',
  mistakes=[["Thinking = means “the answer is next”", "= means the same as."], ["Adding all the numbers", "4 + ☐ = 3 + 6 is not 13."], ["Calling 8 = 3 + 5 false", "The total can be on the left."]],
  faq=[("What does TEKS 1.5E ask?", "Understand that the equal sign represents a relationship where expressions on each side of the equal sign represent the same value(s)."), ("What does TEKS 1.5F ask?", "Determine the unknown whole number in an addition or subtraction equation when the unknown may be any one of the three or four terms in the equation."), ("Is 5 = 5 true?", "Yes. Both sides are 5."), ("How do you find the missing number?", "Make both sides equal.")],
  std="1.5E understand that the equal sign represents a relationship where expressions on each side of the equal sign represent the same value(s); 1.5F determine the unknown whole number in an addition or subtraction equation when the unknown may be any one of the three or four terms in the equation",
  meta="Free Grade 1 worksheets for Texas TEKS 1.5E and 1.5F: the meaning of the equal sign, true or false number sentences and missing numbers. 100 questions with answers.",
  kb="= means both sides have the same value.", ks="4 + 5 = 3 + 6", seo="Grade 1 Equal Sign and Missing Numbers Worksheets (TEKS 1.5E)")

unit(fname="add_three", slug="adding-three-numbers", sort=13, domain=AR, code="1.5G", seed=69113,
  title="Adding Three Numbers", short="Adding Three Numbers",
  doc="Adding three groups with pictures, three numbers within 20, doubles first and any order, and word problems (the US\nGrade 1 makers with Texas names), plus order and grouping (own maker).\nWrong answers come from real mistakes: adding only two of the numbers, counting a number twice, and thinking a new\norder changes the sum.",
  imports=mods(("gen_us_math_g1_add_three", "at")),
  extra=UNIQ + '''

def one_order(r):
    a, b, c = r.sample(range(1, 10), 3)
    s = a + b + c
    if s > 20:
        raise AssertionError
    k = Kid(r).next()
    kind = r.randrange(3)
    if kind == 0:
        return mcq("%d + %d + %d = %d. What is %d + %d + %d?" % (a, b, c, s, c, a, b), str(s), [str(s + 1), str(s - 1), str(a + b)],
                   "Adding in a new order gives the same sum: <b>%d</b>." % s)
    if kind == 1:
        return mcq("Which has the same sum as %d + %d + %d?" % (a, b, c), "%d + %d + %d" % (b, c, a), ["%d + %d" % (a, b), "%d + %d + %d" % (a, b, c + 1), "%d + %d + %d" % (a - 1 if a > 1 else a + 2, b, c)],
                   "Same three numbers in a new order: the sum is still %d." % s)
    return mcq("%s adds %d + %d + %d. %s adds %d + %d first. What does %s get?" % (k["n"], a, b, c, k["He"], b, c, k["he"]), str(s), [str(b + c), str(s + 1), str(a + b)],
               "%d + %d = %d, then %d + %d = <b>%d</b>." % (b, c, b + c, a, b + c, s))
''',
  specs='''        ("Add three groups with pictures", [("run", at.set_pictures, (at.People,), 20)]),
        ("Add three numbers within 20", [("run", at.set_within_20, (at.People,), 20)]),
        ("Doubles first and any order", [("run", at.set_doubles_order, (at.People,), 20)]),
        ("Change the order or the grouping", [("collect", uniq(one_order), 20)]),
        ("Word problems with three numbers", [("run", at.set_word_problems, (at.People,), 20)]),''',
  think="<ul><li>Add two numbers first, then add the third.</li><li>You can add in <b>any order</b>. The sum stays the same.</li><li>Look for a <b>double</b> or a <b>10</b> first: 4 + 7 + 6 = 10 + 7 = 17.</li></ul>",
  examples='example("4 + 7 + 6", ["4 + 6 = 10", "10 + 7"], "17")',
  mistakes=[["Adding only two numbers", "Touch each number as you add it."], ["Counting a number twice", "Cross out each number you use."], ["Thinking a new order changes the sum", "3 + 5 + 2 = 2 + 3 + 5."]],
  faq=[("What does TEKS 1.5G ask?", "Apply properties of operations to add and subtract two or three numbers."), ("Does the order matter when adding?", "No. The sum is the same."), ("What is a good first step?", "Find two numbers that make 10 or a double."), ("Can the sum be more than 20?", "Not on these worksheets.")],
  std="1.5G apply properties of operations to add and subtract two or three numbers",
  meta="Free Grade 1 worksheets for Texas TEKS 1.5G: add three numbers within 20 with pictures, doubles, make 10, any order and word problems. 100 questions with answers.",
  kb="Add in any order; look for 10 or a double first.", ks="4 + 7 + 6 = 10 + 7 = 17", seo="Grade 1 Adding Three Numbers Worksheets (TEKS 1.5G)")
