# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Random Sampling and Inferences (7.SP.A.1, 7.SP.A.2)
  python tools/gen_us_math_g7_random_sampling.py
Populations and samples, random versus biased samples, and using a sample to estimate a population.
Wrong answers come from real mistakes: trusting a convenience sample, using the sample count as the
population count, setting up the proportion upside down, and expecting every sample to give the same result.
"""
import random
from ws_common import (mcq, balance, B, table, example, write_unit)

R = random.Random(71701)
UPDATED = "2026-11-09"


def tf(q, good, bad, e):
    return mcq(q, (good, "g"), [(b, b) for b in bad], e)


def num_item(q, v, ws, e, unit=""):
    show = lambda x: "{:,}".format(x) + unit
    cands = [(show(w), w) for w in list(ws) + [v + 10, v * 2, v // 2] if w > 0 and w != v]
    return mcq(q, (show(v), v), cands, e)


# ------------------------------------------------------------ set 1
def set_words():
    its = []
    pops = [("A school wants to know its 800 students' favorite lunch. It asks 80 students.", "all 800 students", "the 80 students asked"),
            ("A factory checks 50 of the 2,000 light bulbs it made today.", "all 2,000 light bulbs made today", "the 50 bulbs checked"),
            ("A town surveys 300 of its 12,000 voters about a new park.", "all 12,000 voters", "the 300 voters surveyed"),
            ("A biologist catches 40 fish from a lake to study their size.", "all the fish in the lake", "the 40 fish caught")]
    for s, pop, smp in pops:
        its.append(tf(s + " What is the population?", pop, [smp, "the people who run the survey", "only the students who like pizza" if "lunch" in s else "only the largest ones"],
                      "The population is the whole group you want to learn about: %s." % pop))
        its.append(tf(s + " What is the sample?", smp, [pop, "the answers that were most common", "everyone who did not answer"], "The sample is the part of the population you actually study: %s." % smp))
    defs = [("What is a random sample?", "A sample where every member of the population has an equal chance of being chosen",
             ["A sample of the people who are easiest to reach", "A sample of volunteers", "A sample chosen by the teacher's favorite students"],
             "In a random sample, everyone has the same chance, so the sample tends to represent the population."),
            ("Why do we use samples instead of asking everyone?", "Asking everyone can take too much time or cost too much",
             ["Samples are always exactly right", "The population is never important", "Samples do not need to be random"], "A good sample gives a useful estimate with much less work."),
            ("What is a biased sample?", "A sample that does not represent the population well", ["A sample that is too large", "A random sample", "A sample of exactly 100"],
             "A biased sample favors some answers, so its results can be misleading."),
            ("Which word means the sample represents the population?", "Representative", ["Biased", "Convenient", "Voluntary"], "A representative sample has the same kinds of members as the population.")]
    for q, good, bad, e in defs:
        its.append(tf(q, good, bad, e))
    more = [("A larger random sample usually gives…", "a more reliable estimate", ["a biased estimate", "the same answer every time", "a less reliable estimate"],
             "Bigger random samples vary less from the population."),
            ("Two random samples from the same population give slightly different results. Is that normal?", "Yes, random samples vary a little", ["No, the survey must be wrong",
             "No, samples must match exactly", "Only if the samples are biased"], "This is called sampling variability. Results should be close, not identical."),
            ("A sample is used to make a guess about the whole population. This guess is called…", "an inference", ["a census", "a bias", "an outlier"],
             "Using a sample to draw a conclusion about a population is making an inference."),
            ("Asking every member of the population is called…", "a census", ["a sample", "an inference", "a simulation"], "A census collects data from the whole population."),
            ("A sample of 10 people out of 50,000 is…", "probably too small to be reliable", ["always reliable", "a census", "biased only if they are adults"],
             "Very small samples can give results far from the population."),
            ("Which helps make a sample random?", "Drawing names from a hat with every name in it", ["Asking your friends", "Asking people who walk by first",
             "Using people who email in"], "Every name has an equal chance in a fair drawing."),
            ("A study looks at 500 randomly chosen high school students in Ohio. Which population can it describe best?", "High school students in Ohio",
             ["All people in the United States", "Elementary students in Ohio", "Teachers in Ohio"], "A sample can only describe the population it was chosen from."),
            ("What is a numerical fact about a sample, such as its mean, called?", "A statistic", ["A census", "A population", "A bias"],
             "A statistic describes a sample. It is used to estimate a value for the population.")]
    for q, good, bad, e in more:
        its.append(tf(q, good, bad, e))
    return {"title": "Populations and samples", "items": its[:20]}


# ------------------------------------------------------------ set 2
def set_bias():
    its = []
    cases = [("To find the favorite sport at school, Leo asks the soccer team.", "Biased: the soccer team likes soccer more than most students",
              ["Random: every student could be asked", "Biased: the team is too large", "Random: the team has boys and girls"]),
             ("A store asks customers who are leaving to rate the store.", "Biased: it misses people who do not shop there", ["Random: everyone shops", "Biased: the sample is too large", "Random: customers are chosen by chance"]),
             ("A school picks 50 student ID numbers using a random number generator.", "Random: every student has the same chance", ["Biased: computers cannot choose", "Biased: 50 is too many", "Random only if the students volunteer"]),
             ("A TV show asks viewers to call in with their opinion.", "Biased: only people who want to call answer", ["Random: anyone can call", "Random: it is on TV", "Biased: the phone lines are too busy"]),
             ("A city surveys every 10th person on the voter list.", "Random (systematic): the list includes everyone", ["Biased: only 10 people", "Biased: voters only like parks", "Not a sample"]),
             ("To learn how students get to school, Mia asks students on the school bus.", "Biased: bus riders all take the bus", ["Random: the bus is full", "Random: students are on time", "Biased: buses are slow"]),
             ("A gym asks its members how often adults in the town exercise.", "Biased: gym members exercise more than most adults", ["Random: everyone exercises", "Random: the gym is big", "Biased: gyms are closed at night"]),
             ("A teacher puts all 120 names in a box and draws 20.", "Random: every name has an equal chance", ["Biased: 20 is too few", "Biased: the teacher picks", "Random only if 120 are drawn"]),
             ("A website asks visitors to vote in an online poll about video games.", "Biased: visitors choose to answer", ["Random: anyone can vote", "Random: the website is popular", "Biased: polls are short"]),
             ("To find the average height of 7th graders, Omar measures the basketball team.", "Biased: basketball players tend to be taller", ["Random: the team is in 7th grade", "Random: everyone plays", "Biased: the team is small"])]
    for q, good, bad in cases:
        its.append(tf(q + " Is the sample random or biased?", good, bad, "Ask: does every member of the population have the same chance to be chosen?"))
    better = [("Which is the best way to find out what all 600 students want for a class trip?", "Randomly pick 60 students from the school list",
               ["Ask 60 students in the art club", "Ask the first 60 students in line for lunch", "Ask students who volunteer"]),
              ("Which sample best represents the people in a town?", "200 names chosen at random from the town's address list",
               ["200 people at a football game", "200 people at the library", "200 people who answer an online ad"]),
              ("Which question is NOT biased?", "What is your favorite season?", ["Don't you agree that summer is the best season?", "Isn't winter too cold to enjoy?",
               "Most people love spring. Do you?"]),
              ("A survey asks: 'Do you support the great new park that everyone loves?' What is the problem?", "The question pushes people toward 'yes'",
               ["The question is too short", "Parks are not important", "There is no problem"]),
              ("Which sample is most likely to show how all 7th graders feel about homework?", "Every 5th student on an alphabetical list of all 7th graders",
               ["Students in the homework club", "Students staying after school", "Students who finish homework early"]),
              ("A company wants to test 100 phones out of 10,000. Which method is best?", "Choose 100 serial numbers at random", ["Test the first 100 made",
               "Test the 100 that are easiest to reach", "Test phones customers returned"]),
              ("Why might a survey of only people at a pet store be biased about how many families have pets?", "People at a pet store are more likely to have pets",
               ["Pet stores are small", "Pets cannot answer", "It is not biased"]),
              ("A student wants to know the favorite fruit of people in her town. Which is a good sample?", "People chosen at random from the town phone list",
               ["Her family", "Her soccer team", "Shoppers at a fruit stand"]),
              ("Which change makes a sample less biased?", "Choosing people at random from the whole population", ["Asking only friends", "Asking fewer people",
               "Asking a leading question"]),
              ("A news site reports that 90% of 50 readers who commented liked an article. Why is this weak evidence for all readers?", "Only readers who chose to comment are counted",
               ["50 is too large", "90% is too high to be possible", "Comments are always negative"])]
    for q, good, bad in better:
        its.append(tf(q, good, bad, "A good sample is random and from the whole population, and the question does not push people toward an answer."))
    return {"title": "Random or biased?", "items": its}


# ------------------------------------------------------------ set 3: estimate from a sample
def set_estimate():
    its = []
    cases = [(40, 12, 500, "students", "like rock music"), (50, 18, 800, "students", "walk to school"), (60, 15, 1200, "voters", "support the plan"),
             (80, 20, 2000, "people", "own a bike"), (25, 4, 750, "bulbs", "are broken"), (100, 35, 3000, "fans", "buy a T-shirt"),
             (30, 9, 450, "students", "play an instrument"), (200, 14, 5000, "phones", "have a problem"), (75, 30, 900, "students", "prefer pizza"),
             (40, 26, 600, "shoppers", "use a list"), (120, 18, 4800, "trees", "have a disease"), (20, 7, 360, "students", "read every day")]
    for n_, k, N, who, what in cases:
        est = k * N // n_
        assert k * N % n_ == 0
        its.append(num_item("In a random sample of %d %s, %d %s. There are %s %s in all. About how many %s?" % (n_, who, k, what, "{:,}".format(N), who, what),
                            est, [k, N - est, n_ * N // k if n_ * N % k == 0 else est + 50],
                            "%d out of %d is %d/%d. Multiply by the population: %d/%d × %s = %s." % (k, n_, k, n_, k, n_, "{:,}".format(N), "{:,}".format(est))))
    pct = [(50, 30, "%", 60), (40, 10, "%", 25), (80, 52, "%", 65), (200, 46, "%", 23)]
    for n_, k, _, p in pct:
        its.append(num_item("In a random sample of %d people, %d chose blue as their favorite color. What percent of the sample is that?" % (n_, k), p,
                            [k, 100 - p, n_ - k], "%d ÷ %d = %s = %d%%." % (k, n_, "{:.2f}".format(k / n_).rstrip("0").rstrip("."), p), "%"))
    tag = [(50, 200, 5, 2000), (30, 60, 6, 300), (40, 80, 4, 800), (100, 150, 10, 1500)]
    for tagged, catch, recap, N in tag:
        its.append(num_item("Rangers tag %d deer and let them go. Later they see %d deer, and %d are tagged. About how many deer live in the park?" % (tagged, catch, recap), N,
                            [tagged + catch, catch * recap, tagged * recap], "%d of %d seen are tagged, so tagged deer are %d/%d of all deer. %d ÷ (%d/%d) = %s." % (
                                recap, catch, recap, catch, tagged, recap, catch, "{:,}".format(N))))
    return {"title": "Estimate a population from a sample", "items": its}


# ------------------------------------------------------------ set 4: variation in samples
def set_variation():
    its = []
    samples = [[12, 15, 13, 14], [22, 25, 20, 23], [8, 10, 9, 13]]
    for s in samples:
        mean = sum(s) / len(s)
        ans = "%g" % mean
        its.append(tf("Four random samples of 50 students gave these numbers who like hiking: %s. What is a good estimate for one sample of 50?" % ", ".join(map(str, s)),
                      "About %s students" % ans, ["Exactly %d students" % s[0], "About %d students" % (max(s) + min(s)), "About %d students" % sum(s)],
                      "Use the mean of the samples: (%s) ÷ 4 = %s." % (" + ".join(map(str, s)), ans)))
    var = [("Sample A of 20 people found 40% like jazz. Sample B of 20 people found 50%. What does this show?", "Random samples vary, so results differ a little",
            ["One sample must be wrong", "Exactly 45% of people like jazz", "Jazz is getting more popular"]),
           ("Which group of samples gives the most reliable estimate?", "Ten random samples of 100", ["One sample of 10", "Two samples of 20 friends", "One sample of volunteers"]),
           ("Samples of 10 gave 3, 6, 1 and 8. Samples of 100 gave 42, 45, 40 and 44. What do you notice?", "The larger samples are closer together",
            ["The smaller samples are more reliable", "The two sizes vary the same", "Larger samples are biased"]),
           ("Many random samples give means of 61, 63, 60, 62 and 64. Which is the best estimate of the population mean?", "About 62",
            ["Exactly 64", "About 50", "About 310"]),
           ("A random sample of 40 shows 25% chose art. A second random sample of 40 shows 30%. Which estimate of the population is reasonable?", "Between 25% and 30%",
            ["Exactly 25%", "Exactly 55%", "Less than 10%"]),
           ("What is the main reason to take several random samples?", "To see how much the results vary", ["To make the samples biased", "To avoid doing math", "To ask the same people again"]),
           ("A sample mean of 8 hours of sleep is close to the means of 5 other samples. What can you say?", "The estimate is fairly reliable", ["The estimate is biased",
            "Everyone sleeps exactly 8 hours", "The samples were too large"]),
           ("Two samples of 30 apples have mean weights 152 g and 158 g. Which is the best single estimate?", "About 155 g", ["Exactly 152 g", "About 310 g", "About 6 g"])]
    for q, good, bad in var:
        its.append(tf(q, good, bad, "Random samples give slightly different results. Several larger samples help you see how close the estimate is."))
    dots = [("The means of 6 random samples are 4, 5, 5, 6, 5, 5. Which value is the best estimate for the population mean?", "5", ["4", "6", "30"]),
            ("The percents from 5 random samples are 18%, 22%, 20%, 21% and 19%. What is a reasonable estimate for the population?", "About 20%", ["About 100%", "About 2%", "Exactly 18%"]),
            ("A sample's mean is much higher than 9 other samples' means. What might explain it?", "That sample happened to include unusual values", ["The other 9 are wrong",
             "Means cannot vary", "The population changed"]),
            ("Samples of size 5 are spread out a lot. Samples of size 50 are close together. Which size should you trust more?", "Size 50", ["Size 5", "Both equally", "Neither"]),
            ("The spread of results from many samples shows…", "how much an estimate might be off", ["the exact population value", "that sampling is wrong", "the sample size"]),
            ("Which estimate is better: one sample of 400 random students, or one sample of 40 students in a club?", "The sample of 400 random students",
             ["The club sample", "They are the same", "Neither is useful"]),
            ("Ten random samples all show that between 70% and 76% of students eat breakfast. What can you infer?", "About 70% to 76% of all students eat breakfast",
             ["Exactly 73% of students eat breakfast", "Fewer than half eat breakfast", "Nothing"]),
            ("Is it reasonable that a random sample of 100 adults shows 52% like coffee when the true value is 55%?", "Yes, a small difference is normal",
             ["No, it must be exactly 55%", "No, the sample is biased", "Only if the sample is larger than the population"]),
            ("Which statement is true about random samples?", "Different random samples can give different results", ["Every random sample gives the same result",
             "A random sample is always biased", "Random samples cannot be used to estimate"])]
    for q, good, bad in dots:
        its.append(tf(q, good, bad, "Results from random samples vary a little. Look at the middle of several results and how spread out they are."))
    return {"title": "Variation between samples", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_wordprob():
    its = []
    w = [("A random sample of 60 7th graders found 24 have a pet. The school has 420 7th graders. About how many have a pet?", 168, [24, 252, 360]),
         ("A factory finds 3 broken toys in a random sample of 150. It makes 6,000 toys. About how many are broken?", 120, [3, 50, 2000]),
         ("In a random sample of 80 voters, 44 plan to vote yes. There are 10,000 voters. About how many plan to vote yes?", 5500, [44, 4500, 8000]),
         ("A random sample of 25 bags of chips shows 2 are underfilled. In a shipment of 1,500 bags, about how many are underfilled?", 120, [2, 750, 60]),
         ("A school of 900 students: a random sample of 45 shows 15 buy lunch. About how many students buy lunch?", 300, [15, 600, 450]),
         ("Out of 40 randomly chosen library books, 6 are overdue. The library has 2,400 books out. About how many are overdue?", 360, [6, 2040, 400]),
         ("A random sample of 120 people finds 30 read the news daily. In a city of 48,000, about how many read the news daily?", 12000, [30, 36000, 1600]),
         ("A survey of 50 random students found 35 want a longer lunch. Out of 700 students, about how many want a longer lunch?", 490, [35, 210, 1000]),
         ("A farmer tests 20 random apples and finds 1 has a worm. About how many of 1,200 apples have worms?", 60, [1, 1140, 20]),
         ("A random sample of 90 phones finds 9 need repair. Out of 3,600 phones, about how many need repair?", 360, [9, 400, 3240])]
    for q, v, ws in w:
        parts = [int(x.replace(",", "")) for x in __import__("re").findall(r"\d[\d,]*", q)]
        its.append(num_item(q, v, ws, "Find the fraction in the sample, then multiply by the whole group. The estimate is %s." % "{:,}".format(v)))
    concl = [("A random sample of 100 students shows 62% prefer a 4-day week. Which conclusion is reasonable?", "About 60% of all students might prefer a 4-day week",
              ["Exactly 62 students in the school prefer it", "Every student prefers it", "No conclusion is possible"]),
             ("A sample of 30 students in the chess club shows 90% like strategy games. Can you say 90% of the school likes strategy games?", "No, the sample is biased",
              ["Yes, 30 is enough", "Yes, chess is popular", "No, 90% is impossible"]),
             ("A random sample of 200 shoppers shows 1 in 4 uses coupons. A store has 3,000 shoppers a week. About how many use coupons?", "About 750",
              ["About 200", "About 1,200", "About 2,250"]),
             ("A random sample shows students sleep a mean of 8.5 hours, and another shows 8.1 hours. What is a good estimate?", "About 8.3 hours",
              ["Exactly 8.5 hours", "About 16.6 hours", "About 0.4 hours"]),
             ("Fish are tagged: 60 tagged fish are released. Later, 5 of 80 fish caught are tagged. About how many fish are in the lake?", "About 960",
              ["About 140", "About 400", "About 4,800"]),
             ("A city asks 1,000 random residents and finds 18% ride the bus. The city has 250,000 residents. About how many ride the bus?", "About 45,000",
              ["About 180", "About 18,000", "About 205,000"]),
             ("Which sample size is most likely to give an estimate close to the true value?", "500 randomly chosen people", ["5 randomly chosen people",
              "50 friends", "500 volunteers who reply to an ad"]),
             ("A random sample of 40 finds 10 left-handed people. Leo says exactly 25% of the world is left-handed. What is wrong?", "A sample gives an estimate, not an exact value",
              ["The sample should be biased", "25% is too big", "Nothing is wrong"]),
             ("Two random samples of 50 give 14 and 16 students who bike. The school has 500 students. Which estimate is reasonable?", "About 150 students",
              ["About 30 students", "About 300 students", "About 14 students"]),
             ("A random sample of 60 students shows these favorite subjects: math 18, science 15, English 12, art 15. About what fraction of all students prefer math?", "About 3/10",
              ["About 18/100", "About 1/2", "About 1/18"])]
    for q, good, bad in concl:
        its.append(tf(q, good, bad, "Use the sample's fraction or percent as an estimate for the whole population, and check that the sample is random."))
    return {"title": "Word problems: making inferences", "items": its}


def body():
    rows = [["Population", "The whole group", "All 800 students"], ["Sample", "The part you study", "80 students"],
            ["Random sample", "Everyone has an equal chance", "Names drawn from a list of all students"], ["Biased sample", "Favors some answers", "Only the soccer team"]]
    return ("<h2>Populations and samples</h2><p>A <b>population</b> is the whole group you want to learn about. A <b>sample</b> is the part you actually ask. "
            "A <b>random sample</b> gives everyone the same chance to be chosen, so it tends to represent the population.</p>"
            + table(["Word", "Meaning", "Example"], rows)
            + "<h2>Estimate with a sample</h2><p>Find the fraction or percent in the sample, then multiply by the population.</p>"
            + example("In a random sample of 50 students, 18 walk to school. About how many of 800 students walk?", ["18 out of 50 = 0.36.", "0.36 × 800 = 288."], "about 288 students")
            + "<p>Different random samples give slightly different results. Larger samples, and several samples, give more reliable estimates.</p>"
            + "<h2>Common mistakes</h2><ul><li>Trusting a sample that is easy to reach, like your friends or one club.</li>"
            "<li>Using the sample number as the answer for the whole population.</li><li>Thinking an estimate is an exact value.</li></ul>")


def main():
    sets = [set_words(), set_bias(), set_estimate(), set_variation(), set_wordprob()]
    for st in sets:
        for it in st["items"]:
            it["q"] = it["q"].replace("3/10", "3/10")
    balance(sets, R)
    unit = {
        "slug": "random-sampling",
        "title": "Random Sampling and Inferences",
        "seo_title": "Grade 7 Random Sampling Worksheets: Populations, Biased Samples and Making Inferences",
        "short_title": "Random sampling",
        "domain": "Statistics & Probability",
        "standard_code": "7.SP.A.1–2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/SP/A/1/",
        "standard_text": "Understand that statistics can be used to gain information about a population by examining a sample of the population; generalizations about a population from a sample are valid only if the sample is representative of that population. Use data from a random sample to draw inferences about a population with an unknown characteristic of interest.",
        "meta_desc": "Free Grade 7 random sampling worksheets: populations and samples, random versus biased samples, estimating a population from a sample, variation between samples, and making inferences. 100 practice questions with an answer key.",
        "key_big": "A random sample gives everyone the same chance. Use its fraction to estimate the whole population.",
        "key_sub": "18 of 50 sampled walk, so about 18/50 × 800 = 288 of 800 students walk. Bigger random samples are more reliable.",
        "body_html": body(),
        "faq": [
            {"q": "What is the difference between a population and a sample?", "a": "The population is the whole group you want to know about. The sample is the smaller group you actually study."},
            {"q": "What makes a sample biased?", "a": "A sample is biased when some members are more likely to be chosen, like asking only the soccer team about favorite sports, or asking a question that pushes people to one answer."},
            {"q": "How do you estimate a population from a sample?", "a": "Find the fraction or percent in the sample and multiply it by the population. 12 of 40 is 30%, so about 30% of 500 = 150."},
            {"q": "Why do different samples give different results?", "a": "Each random sample includes different people, so results vary a little. Larger samples vary less."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 17,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
