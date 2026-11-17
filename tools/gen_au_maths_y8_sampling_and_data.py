# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Sampling and Data (Australian Curriculum v9.0: AC9M8ST01)
  python3 tools/gen_au_maths_y8_sampling_and_data.py
Census, sample, experiment and observation; random and non-random samples and bias; primary and secondary
data; estimating a population from a sample; sample statistics and outliers; and comparing samples.
Wrong answers come from real mistakes: thinking a bigger sample is always unbiased, choosing a convenient
sample, scaling a sample proportion the wrong way, and letting one outlier decide the mean.
"""
import random
from fractions import Fraction as F
from au_hs import num, B, S, make, lesson, collect, QN, T, dec

R = random.Random(81701)


def n(v):
    v = F(v)
    return num(v) if v.denominator == 1 else dec(v)


# ------------------------------------------------------------ set 1: collecting data
METHODS = [
    ("Every student at a school is asked how they travel to school.", "Census", ["Sample", "Experiment", "Observation"], "Everyone in the population is asked: a <b>census</b>."),
    ("The Australian Bureau of Statistics collects information from every household in Australia every five years.", "Census", ["Sample", "Experiment", "Secondary data only"], "Every household is included: a <b>census</b>."),
    ("100 voters out of 20 000 in a town are asked who they will vote for.", "Sample", ["Census", "Experiment", "Observation"], "Only part of the population is asked: a <b>sample</b>."),
    ("A student counts how many cars pass the school gate between 8 am and 9 am.", "Observation", ["Census", "Experiment", "Survey"], "Watching and recording what happens: an <b>observation</b>."),
    ("Half the tomato plants get a new fertiliser and half do not, and their growth is compared.", "Experiment", ["Observation", "Census", "Sample"], "Changing one thing on purpose and measuring the effect: an <b>experiment</b>."),
    ("A student drops a ball from different heights and measures how high it bounces.", "Experiment", ["Observation", "Census", "Secondary data"], "Changing the height on purpose and measuring: an <b>experiment</b>."),
    ("A scientist records which birds visit a feeder each morning for a month.", "Observation", ["Experiment", "Census", "Sample survey"], "Recording what happens without changing it: an <b>observation</b>."),
    ("A company tests 50 light globes from a batch of 10 000 to see how long they last.", "Sample", ["Census", "Observation", "Secondary data"], "Only some globes are tested (testing all would destroy them): a <b>sample</b>."),
]
WHY = [
    ("Why does a factory test a sample of its matches rather than every match?", "Testing a match destroys it", ["A census is more accurate", "Matches are all the same", "It is against the law to test them all"],
     "A test uses up the match, so testing every one would leave none to sell: <b>testing destroys it</b>."),
    ("What is the main advantage of a census over a sample?", "It includes every member of the population", ["It is cheaper", "It is quicker", "It needs fewer people to run it"], "A census <b>includes everyone</b>, so there is no sampling error."),
    ("What is the main advantage of a sample over a census?", "It is quicker and cheaper", ["It is always more accurate", "It includes everyone", "It cannot be biased"], "A sample is <b>quicker and cheaper</b> than asking everyone."),
    ("Which is primary data?", "Measurements you collect yourself", ["Figures from the Bureau of Meteorology website", "A table in a newspaper", "Results from a census report"],
     "Primary data is <b>collected by you</b>; the others are secondary data."),
    ("Which is secondary data?", "Rainfall records downloaded from the Bureau of Meteorology", ["Heights you measure in your class", "A survey you give to your friends", "Times you record in a race"],
     "Data someone else collected is <b>secondary data</b>."),
    ("A student wants to know if a new playground is used more at lunch than at recess. Which method is most suitable?", "Observation", ["Census of the whole country", "Experiment", "Secondary data from another school"],
     "She can watch and count users at each break: <b>observation</b>."),
    ("Which question is best answered with an experiment?", "Does warm water dissolve sugar faster than cold water?", ["What is the most popular sport at school?", "How many people live in Perth?", "How many birds visit a tree?"],
     "You can change the water temperature and measure the effect: <b>an experiment</b>."),
    ("A census of Australia is expensive. Why is it still carried out?", "Governments need accurate information about everyone to plan services", ["A sample is never accurate", "It is the only way to get data", "It is cheaper than a sample"],
     "Planning schools, hospitals and roads needs <b>accurate information about everyone</b>."),
    ("Which is NOT a practical problem with a census?", "It only includes part of the population", ["It costs a lot", "It takes a long time", "Some people may not respond"], "A census includes everyone, so <b>only part of the population</b> is not one of its problems."),
    ("Why might observation data about animals be better than asking people about them?", "People's memories and opinions can be inaccurate", ["Animals can fill in surveys", "Observation is always faster", "Observation needs no planning"],
     "Watching gives first-hand data, while <b>people's memories and opinions can be inaccurate</b>."),
    ("A researcher wants to know the average height of Year 8 students in Australia. What is most practical?", "Measure a random sample of Year 8 students", ["Measure every Year 8 student", "Measure her own class only", "Use the heights of adults"],
     "A census would be huge; a <b>random sample</b> is practical and fair."),
    ("Which describes the population in a survey about the reading habits of students at Riverside High?", "All students at Riverside High", ["The students who answer the survey", "All Australians", "Only the Year 8 students"], "The population is the whole group you want to know about: <b>all students at Riverside High</b>."),
]


# ------------------------------------------------------------ set 2: random and non-random samples, bias
BIAS = [
    ("To find the most popular sport at school, Jack asks the members of the football team. Why is this sample biased?", "Football players are likely to choose football", ["The sample is random", "The sample is too large", "Sport is not a fair question"],
     "The people asked are not typical of the school: <b>football players are likely to choose football</b>."),
    ("To find how far people travel to work, a survey is given out at a train station. Why might it be biased?", "It leaves out people who drive, walk or cycle", ["Train stations are too busy", "It is a census", "It includes too many people"],
     "Only train users are asked, so <b>people who drive, walk or cycle are left out</b>."),
    ("Which is a random sample of 50 students from a school of 800?", "Put all 800 names in a computer and select 50 at random", ["Ask the first 50 students through the gate", "Ask 50 students in the library", "Ask 50 volunteers"],
     "In a random sample every student has the same chance: <b>select 50 at random from all 800 names</b>."),
    ("A TV show asks viewers to text in their opinion. What kind of sample is this?", "A self-selected (non-random) sample", ["A random sample", "A census", "A systematic sample"], "Only viewers who choose to reply are counted: <b>self-selected</b>."),
    ("Which is a systematic sample?", "Choosing every 10th name on the class roll", ["Choosing names out of a hat", "Asking your friends", "Asking anyone who walks past"], "Choosing at regular intervals: <b>systematic</b>."),
    ("A survey about a new skate park is handed out at a skate shop. What is the problem?", "Skaters are more likely to want a skate park", ["The survey is too short", "The sample is random", "Skate shops have few customers"],
     "The sample is not representative: <b>skaters are more likely to want a skate park</b>."),
    ("Which question is biased?", "Don't you agree that school should start later?", ["What time would you like school to start?", "How do you travel to school?", "How many hours of sleep do you get?"],
     "<b>Don't you agree…</b> pushes people towards one answer."),
    ("A sample of 1000 people is chosen only from Sydney to represent all Australians. What is the main problem?", "It does not represent people from other places", ["1000 is too small", "1000 is too large", "It is a census"],
     "A large sample can still be biased: <b>it does not represent people from other places</b>."),
    ("How can you reduce bias in a sample?", "Choose people at random from the whole population", ["Ask only people you know", "Ask only people who volunteer", "Ask people in one place"], "<b>Random selection</b> from the whole population gives everyone the same chance."),
    ("Why is a convenience sample (asking whoever is nearby) often not reliable?", "The people nearby may not be typical of the population", ["It is always too large", "It is random", "It takes too long"], "Convenient people may share habits: <b>they may not be typical</b>."),
    ("Which sample is most likely to represent all students in a school of 1200?", "A random sample of 100 students from the whole school", ["All 30 students in one Year 12 class", "100 students at a chess club", "The first 100 students to reply to an email"],
     "A <b>large random sample from the whole school</b> is most representative."),
    ("A council wants residents' views on a new library. Which sample is least biased?", "A random selection of addresses from the electoral roll", ["People already in the library", "People who answer an online poll", "People at a book shop"],
     "<b>Random addresses</b> give every resident an equal chance."),
    ("Two classes each take a random sample of 20 students. Will they get exactly the same results?", "Probably not, because samples vary", ["Yes, always", "Only if they ask the same questions", "No, because one sample must be biased"],
     "Different random samples give different results: <b>samples vary</b>."),
    ("Which happens to the variation between random samples as the sample size increases?", "It usually gets smaller", ["It gets bigger", "It stays exactly the same", "It disappears for any sample over 10"], "Larger random samples usually <b>vary less</b>, so they are more reliable."),
    ("A stratified sample of 60 students is taken from a school with 300 boys and 300 girls. How many girls should be chosen?", "30", ["60", "20", "300"], "Girls are half the school, so half the sample: <b>30</b>."),
    ("A survey asks 'How much do you love our delicious new burger?' What is wrong with it?", "It is a leading question", ["It is too short", "It is a census", "It uses a random sample"], "The words <b>lead</b> people to a positive answer."),
    ("Which is non-random sampling?", "Asking people who walk past at a shopping centre", ["Rolling a die to choose students", "Using a random number generator", "Drawing names from a hat"], "Choosing whoever walks past is <b>non-random</b> (convenience)."),
    ("Ruby surveys 10 of her friends and finds that 9 like pineapple on pizza. She says 90% of Australians like it. What is the main problem?", "Her sample is small and not random", ["90% is too high", "She should have used a census", "Pizza is not a fair topic"],
     "Ten friends are a <b>small, non-random</b> sample."),
    ("Online reviews of a restaurant are mostly very good or very bad. Why?", "People with strong feelings are more likely to write a review", ["The restaurant is random", "Reviews are a census", "Everyone writes a review"],
     "A self-selected sample attracts <b>people with strong feelings</b>."),
    ("Which sample size is most likely to give a reliable estimate, if all are chosen at random?", "400", ["4", "20", "40"], "Larger random samples are more reliable: <b>400</b>."),
]


# ------------------------------------------------------------ set 3: estimating from a sample
def one_est(r):
    kind = r.choice(["school", "fish", "town", "pct"])
    if kind == "school":
        N = r.choice([600, 800, 900, 1000, 1200, 1500])
        s = r.choice([40, 50, 60, 75, 100])
        k = r.randint(4, s - 5)
        est = F(N * k, s)
        if est.denominator != 1:
            return None
        act = r.choice(["walk to school", "play a musical instrument", "have a pet dog", "catch the bus"])
        q = "In a random sample of %d students from a school of %s, %d %s. Estimate how many students in the whole school %s." % (s, num(N), k, act, act)
        e = "%d out of %d is %s of the sample. %s × %s = <b>%s</b>." % (k, s, n(F(k, s)), n(F(k, s)), num(N), num(est))
        return QN(q, est, [F(N * s, k) if (F(N * s, k)).denominator == 1 else N - est, F(k * N, 100), N - est], e, near=(10, -10, 20))
    if kind == "town":
        N = r.choice([5000, 8000, 12000, 20000, 25000, 40000])
        s = r.choice([200, 250, 400, 500])
        k = r.randint(s // 10, s // 2) // 5 * 5
        est = F(N * k, s)
        if est.denominator != 1:
            return None
        q = "A random sample of %d adults in a town of %s finds that %d want a new swimming pool. Estimate how many adults in the town want the pool." % (s, num(N), k)
        e = "%d ÷ %d = %s. %s × %s = <b>%s</b>." % (k, s, n(F(k, s)), n(F(k, s)), num(N), num(est))
        return QN(q, est, [N - est, k * 10, F(N, s) + k], e, near=(100, -100, 500))
    if kind == "pct":
        p = r.choice([5, 8, 12, 15, 20, 24, 35, 40, 45])
        N = r.choice([500, 1200, 2000, 2500, 3000])
        est = F(N * p, 100)
        q = "In a random sample, %d%% of the trees in a forest have a disease. The forest has %s trees. Estimate how many have the disease." % (p, num(N))
        e = "%d%% of %s = %s × %s = <b>%s</b>." % (p, num(N), n(F(p, 100)), num(N), num(est))
        return QN(q, est, [N - est, F(N, p) if F(N, p).denominator == 1 else p * 10, est * 10], e, near=(10, -10, 50))
    tagged = r.choice([30, 40, 50, 60, 80])
    caught = r.choice([40, 50, 60, 80, 100])
    marked = r.randint(4, 12)
    est = F(tagged * caught, marked)
    if est.denominator != 1:
        return None
    q = ("Rangers catch %d fish in a lake, tag them and release them. Later they catch %d fish and %d are tagged. "
         "Estimate the number of fish in the lake." % (tagged, caught, marked))
    e = "%d out of %d caught are tagged, so the %d tagged fish are about %d/%d of the lake. %d × %d ÷ %d = <b>%s</b>." % (marked, caught, tagged, marked, caught, tagged, caught, marked, num(est))
    return QN(q, est, [tagged + caught, F(tagged * marked, caught) if F(tagged * marked, caught).denominator == 1 else tagged + caught - marked, caught - marked], e)


# ------------------------------------------------------------ set 4: sample statistics
def one_stat(r):
    k = r.choice([5, 6, 7])
    data = [r.randint(2, 20) for _ in range(k)]
    kind = r.choice(["mean", "median", "range", "outlier"])
    srt = sorted(data)
    shown = ", ".join(str(x) for x in data)
    ctx = r.choice(["goals scored by a netball team in %d games" % k, "text messages sent in a day by %d students" % k, "books read last term by %d students" % k])
    if kind == "mean":
        m = F(sum(data), k)
        if m.denominator not in (1, 2, 5, 10, 4):
            return None
        q = "A sample shows the %s: %s. What is the mean?" % (ctx, shown)
        return QN(q, m, [F(sum(data), k - 1) if F(sum(data), k - 1).denominator in (1, 2, 4, 5) else None, srt[k // 2], sum(data)], "Total = %d, and %d ÷ %d = <b>%s</b>." % (sum(data), sum(data), k, n(m)), fmt=n, near=(1, -1))
    if kind == "median":
        med = F(srt[k // 2]) if k % 2 else F(srt[k // 2 - 1] + srt[k // 2], 2)
        q = "A sample shows the %s: %s. What is the median?" % (ctx, shown)
        e = "In order: %s. The middle %s <b>%s</b>." % (", ".join(map(str, srt)), "value is" if k % 2 else "two values average to", n(med))
        return QN(q, med, [F(data[k // 2]) if k % 2 else F(data[k // 2 - 1] + data[k // 2], 2), F(sum(data), k), srt[-1] - srt[0]], e, fmt=n, near=(1, -1))
    if kind == "range":
        rg = srt[-1] - srt[0]
        q = "A sample shows the %s: %s. What is the range?" % (ctx, shown)
        return QN(q, rg, [srt[-1], data[-1] - data[0] if data[-1] - data[0] != rg else rg + 2, srt[-1] + srt[0]], "Range = largest − smallest = %d − %d = <b>%d</b>." % (srt[-1], srt[0], rg))
    big = r.choice([60, 75, 90, 120])
    d2 = data + [big]
    m1, m2 = F(sum(data), k), F(sum(d2), k + 1)
    if m1.denominator != 1 or m2.denominator != 1:
        return None
    q = "The mean of the sample %s is %s. A new value of %d is added. What is the new mean?" % (shown, num(m1), big)
    e = "New total = %d + %d = %d, and %d ÷ %d = <b>%s</b>. One outlier has raised the mean a lot." % (sum(data), big, sum(d2), sum(d2), k + 1, num(m2))
    return QN(q, m2, [F(sum(d2), k), m1 + big, F(m1 + big, 2)], e, fmt=n, near=(1, -1))


# ------------------------------------------------------------ set 5: comparing samples
def problems():
    data = [
        ("Sample A of 20 students has a mean height of 158 cm. Sample B of 200 students has a mean of 156 cm. Which is likely to be closer to the mean of the whole year group?", "Sample B",
         ["Sample A", "They are equally reliable", "Neither can be used"], "Larger random samples are usually more reliable: <b>Sample B</b>."),
        ("Five random samples of 10 students give the proportion who walk to school as 0.3, 0.5, 0.2, 0.4 and 0.6. What is the mean of these proportions?", "0.4", ["0.2", "0.5", "2"], "(0.3 + 0.5 + 0.2 + 0.4 + 0.6) ÷ 5 = <b>0.4</b>."),
        ("In the five samples above, what is the range of the proportions?", "0.4", ["0.6", "0.2", "0.3"], "0.6 − 0.2 = <b>0.4</b>."),
        ("If the samples above had 100 students each instead of 10, what would you expect?", "The proportions would vary less", ["The proportions would vary more", "Every sample would give 0.4", "The mean would be 4"],
         "Larger samples usually <b>vary less</b>."),
        ("A sample's data is 3, 4, 4, 5, 5, 6, 48. Which is the best measure of a typical value?", "The median, because 48 is an outlier", ["The mean, because it uses every value", "The range", "The mode, because 4 and 5 both appear twice"],
         "One outlier pulls the mean up to 10.7. <b>The median (5)</b> is more typical."),
        ("Two samples of Year 8 test scores have the same mean of 65. Sample A has a range of 20 and Sample B has a range of 60. What does this tell you?", "Sample B's scores are more spread out", ["Sample A's scores are higher", "Sample B's scores are higher", "Both samples are the same"],
         "A larger range means the scores are <b>more spread out</b>."),
        ("A sample of 50 Year 8 students finds 12 are left-handed. What percentage is this?", "24%", ["12%", "38%", "50%"], "12 ÷ 50 × 100 = <b>24%</b>."),
        ("A sample of 40 from School A finds 10 cycle to school. A sample of 60 from School B finds 12 cycle. Which school's sample has the greater proportion of cyclists?", "School A",
         ["School B", "They are the same", "You cannot compare different sample sizes"], "A: 10 ÷ 40 = 25%. B: 12 ÷ 60 = 20%. <b>School A</b>."),
        ("Which data is categorical?", "Favourite colour", ["Height in cm", "Number of siblings", "Time to run 100 m"], "<b>Favourite colour</b> is a category, not a number."),
        ("Which data is continuous numerical?", "Time to run 100 m", ["Number of pets", "Favourite fruit", "Shoe brand"], "Time can take any value in a range: <b>continuous</b>."),
        ("Which data is discrete numerical?", "Number of siblings", ["Height", "Mass", "Favourite movie"], "You count siblings in whole numbers: <b>discrete</b>."),
        ("The ages of a random sample of people at a beach are mostly 15 to 30, with a few older people. How would you describe the distribution?", "Skewed, with a tail of older ages", ["Symmetrical", "Every age is equally common", "It has no outliers"],
         "Most values are low with a few high ones: <b>skewed, with a tail of older ages</b>."),
        ("A random sample of 80 apples from an orchard has 6 bruised apples. The orchard has 4000 apples. Estimate the number of bruised apples.", "300", ["6", "480", "3700"], "6 ÷ 80 = 0.075. 0.075 × 4000 = <b>300</b>."),
        ("Which statement about samples is TRUE?", "A random sample can still give a result that differs from the population", ["A random sample always matches the population exactly", "A biased sample is fine if it is large", "A census is a type of sample"],
         "Random samples vary, so <b>a sample can differ from the population</b>."),
        ("A survey of 30 people at a gym finds they exercise 6 hours a week on average. Why should this not be used for all adults?", "Gym members probably exercise more than most adults", ["30 is too many", "The mean is wrong", "Adults never exercise"],
         "The sample is biased: <b>gym members probably exercise more</b>."),
        ("Which graph best shows how a sample of heights is distributed?", "A histogram or dot plot", ["A pie chart", "A line graph of height against date", "A single bar"], "A <b>histogram or dot plot</b> shows the shape and spread of numerical data."),
        ("The median number of hours of screen time in a sample is 3. What does this mean?", "Half the sample had 3 hours or less", ["Everyone had 3 hours", "The average of the highest and lowest is 3", "3 was the most common value"],
         "The median is the middle value, so <b>half the sample had 3 hours or less</b>."),
        ("A sample of 25 students has a mean of 12 books read. The total for the sample is…", "300", ["37", "12", "2.08"], "Total = mean × number = 12 × 25 = <b>300</b>."),
        ("In a sample, the mean is much larger than the median. What does this suggest?", "There are some very large values", ["There are some very small values", "The data is symmetrical", "There is no spread"],
         "A few very large values pull the mean up: <b>there are some very large values</b>."),
        ("Why do researchers often take several random samples instead of one?", "To see how much the results vary", ["To make the results biased", "To avoid using random selection", "Because one sample is always wrong"],
         "Several samples show <b>how much results vary</b>, which helps judge reliability."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>census</b> collects data from every member of a population; a <b>sample</b> collects data from part of it. "
        "Data can also come from an <b>experiment</b> (changing something on purpose) or an <b>observation</b> (watching and recording). "
        "Data you collect is <b>primary</b>; data someone else collected is <b>secondary</b>.</p>"
        "<p>A <b>random sample</b> gives everyone the same chance of being chosen. Non-random samples, such as asking your friends or "
        "whoever volunteers, are often <b>biased</b>. Larger random samples usually vary less.</p>"
        "<p>To estimate a population, use the sample proportion: (number in sample ÷ sample size) × population.</p>",
        [("In a random sample of 50 students, 18 play an instrument. Estimate the number in a school of 800.", ["18 ÷ 50 = 0.36.", "0.36 × 800."], "288 students"),
         ("Is asking 20 people at a dog park whether they like dogs a fair sample?", ["People at a dog park probably like dogs."], "No, it is biased")],
        ["Thinking a large sample cannot be biased. A large sample from one group is still biased.",
         "Choosing a convenient sample, such as your friends, instead of a random one.",
         "Scaling the wrong way: if 9 out of 30 is the sample, multiply the population by 9/30, not 30/9.",
         "Using the mean when an outlier makes it untypical. The median may be better."])


def main():
    m = [T(q, a, w, e) for q, a, w, e in METHODS + WHY]
    sets = [S("Census, sample, experiment and observation", m),
            S("Random samples and bias", [T(q, a, w, e) for q, a, w, e in BIAS]),
            S("Estimating from a sample", collect(one_est, 20, R)),
            S("Sample statistics", collect(one_stat, 20, R)),
            S("Comparing samples and distributions", problems())]
    make(8, "sampling-and-data", 17, "AC9M8ST01",
         "Sampling and Data: Census, Samples, Bias and Estimates",
         "Year 8 Sampling Worksheets: Census, Random Samples, Bias and Estimating Populations (Free, Answer Key)",
         "Sampling and data",
         "investigate techniques for data collection including census, sampling, experiment and observation, and explain the "
         "practicalities and implications of obtaining data through these techniques",
         "Free Year 8 maths worksheets on sampling for the Australian Curriculum (AC9M8ST01): census, sample, experiment and observation, "
         "random and non-random samples, bias, estimating a population and comparing samples. 100 questions with an answer key.",
         "A random sample gives everyone the same chance of being chosen.",
         "A sample can estimate a population: sample proportion × population size.",
         body(),
         [("What is the difference between a census and a sample?", "A census collects data from every member of the population. A sample collects data from only part of it."),
          ("What makes a sample biased?", "A sample is biased when some groups are more likely to be chosen than others, for example asking only your friends or only people at one place."),
          ("How do I estimate a population from a sample?", "Find the fraction of the sample with the feature, then multiply it by the size of the population."),
          ("Why do different samples give different results?", "Each random sample includes different people, so results vary. Larger samples usually vary less.")],
         sets, R)


if __name__ == "__main__":
    main()
