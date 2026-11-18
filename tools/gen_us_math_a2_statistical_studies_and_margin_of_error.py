# -*- coding: utf-8 -*-
"""
US Algebra 2: Statistical Studies and Margin of Error (Common Core S-IC.A.1, S-IC.B.3, S-IC.B.4, S-IC.B.5)
  python3 tools/gen_us_math_a2_statistical_studies_and_margin_of_error.py
Surveys, observational studies and experiments; sampling methods and bias; the margin of error 1/√n;
confidence intervals; and randomized experiments and simulations.
Wrong answers come from real mistakes: calling an observational study an experiment, trusting a voluntary
response sample, thinking a bigger margin of error is more precise, and claiming cause from correlation.
"""
import math
import random
from us_hs import B, S, make, lesson, collect, T, num, MINUS, People

R = random.Random(96601)
TYPES = ["Sample survey", "Observational study", "Experiment"]


# ------------------------------------------------------------ set 1: type of study
STUDIES = [
    ("A researcher asks 500 randomly chosen voters which candidate they prefer.", "Sample survey"),
    ("Doctors compare the health records of people who already drink coffee with people who do not.", "Observational study"),
    ("Students are randomly assigned to study with music or in silence, and their test scores are compared.", "Experiment"),
    ("A biologist records how many birds visit feeders in different parks without changing anything.", "Observational study"),
    ("A company randomly gives half of its stores a new layout and compares sales with the other half.", "Experiment"),
    ("A school sends a questionnaire to a random sample of parents about lunch options.", "Sample survey"),
    ("Researchers watch whether drivers who use phones have more accidents, using police reports.", "Observational study"),
    ("Volunteers are randomly assigned to take a new vitamin or a placebo for 8 weeks.", "Experiment"),
    ("A city calls 1,000 random households to ask how many people live in each home.", "Sample survey"),
    ("A farmer randomly assigns plots to two fertilizers and measures the crop yield.", "Experiment"),
    ("A study compares grades of students who chose to take music lessons with those who did not.", "Observational study"),
    ("A website asks a random sample of users to rate their satisfaction from 1 to 5.", "Sample survey"),
    ("A team randomly assigns runners to two kinds of shoes and compares their race times.", "Experiment"),
    ("Researchers record the screen time and sleep of 300 teens without changing their habits.", "Observational study"),
    ("A pollster asks 1,200 randomly chosen adults whether they own an electric car.", "Sample survey"),
    ("A teacher randomly assigns half of her classes to online homework and half to paper homework, then compares scores.", "Experiment"),
    ("Scientists compare lung health in people who already live near highways with people who live far away.", "Observational study"),
    ("A library emails a random sample of members to ask how often they visit.", "Sample survey"),
    ("Patients are randomly assigned to one of three doses of a medicine, and blood pressure is measured.", "Experiment"),
    ("An ecologist counts the frogs in ponds with and without fish, without changing the ponds.", "Observational study"),
]


def one_type(r):
    if r.random() < 0.75:
        s, right = r.choice(STUDIES)
        why = {"Sample survey": "Data are collected by asking a sample questions; nothing is assigned.",
               "Observational study": "The researcher observes groups that already exist and does not assign a treatment.",
               "Experiment": "The researcher assigns treatments (randomly) and measures the effect."}[right]
        return T("What type of study is this? %s" % s, right, [x for x in TYPES if x != right] + ["Census"], why + " <b>%s</b>." % right)
    items = [("Which type of study can show that one variable causes a change in another?", "A randomized experiment", ["An observational study", "A sample survey", "A census"],
              "Only random assignment of treatments balances the other factors, so differences can be blamed on the treatment."),
             ("A study finds that people who sleep more have higher grades. Can we say sleep causes higher grades?", "No, it is an observational study, so it shows only an association",
              ["Yes, because the result was large", "Yes, because the sample was random", "No, because grades cannot be measured"],
              "Other factors could explain both. Without random assignment, correlation does not show causation."),
             ("What is a census?", "Collecting data from every member of the population", ["Collecting data from a random sample", "Assigning treatments at random", "Asking only volunteers"],
              "A census includes the whole population, not a sample."),
             ("Why do experiments use a control group?", "To compare the treatment with no treatment (or a placebo)", ["To make the sample bigger", "To remove all bias from surveys", "To pick volunteers"],
              "The control group shows what happens without the treatment, so the effect can be measured.")]
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 2: sampling methods and bias
METHODS = [
    ("Each student's ID number is put into a computer, which picks 50 at random.", "Simple random sample"),
    ("The school picks 10 students at random from each grade.", "Stratified sample"),
    ("A researcher randomly chooses 5 classrooms and surveys every student in them.", "Cluster sample"),
    ("A store surveys every 20th customer who walks in.", "Systematic sample"),
    ("A reporter interviews the first 30 people she meets at a mall.", "Convenience sample"),
    ("A TV show asks viewers to call in and vote.", "Voluntary response sample"),
    ("A town randomly picks 3 neighborhoods and surveys every household in them.", "Cluster sample"),
    ("A factory tests every 100th item that comes off the line.", "Systematic sample"),
    ("A website posts a poll and anyone who visits can answer.", "Voluntary response sample"),
    ("A company randomly chooses 20 workers from each department.", "Stratified sample"),
    ("Names are drawn from a hat holding the name of every member of a club.", "Simple random sample"),
    ("A teacher asks the students sitting in the front row.", "Convenience sample"),
    ("A magazine prints a survey and readers can mail it back if they want.", "Voluntary response sample"),
    ("A pollster randomly picks 100 voters from each county in the state.", "Stratified sample"),
    ("An airline randomly picks 8 flights and surveys every passenger on them.", "Cluster sample"),
    ("Starting at a random name, a coach chooses every 10th name on the team list.", "Systematic sample"),
    ("A random number generator picks 200 phone numbers from a list of all customers.", "Simple random sample"),
    ("A researcher surveys the people in her own neighborhood because they are easy to reach.", "Convenience sample"),
]


def one_samp(r):
    if r.random() < 0.7:
        s, right = r.choice(METHODS)
        names = ["Simple random sample", "Stratified sample", "Cluster sample", "Systematic sample", "Convenience sample", "Voluntary response sample"]
        wr = [n for n in names if n != right]
        r.shuffle(wr)
        return T("Which sampling method is described? %s" % s, right, wr[:3], "<b>%s</b>." % right)
    items = [("Which sample is most likely to be biased?", "People who choose to answer an online poll", ["A computer-chosen random sample of all residents", "10 random students from each grade",
              "Every 25th name from a complete list, starting at random"], "Voluntary responders often have strong opinions, so they do not represent everyone."),
             ("A survey about a new park is given only to people already at the park. What is the problem?", "The sample is not representative of all residents",
              ["The sample is too random", "The questions are not numerical", "There is no problem"], "People at the park probably like parks more than others: this is a biased, convenience sample."),
             ("Which question is worded in a biased way?", "Don't you agree that the unfair tax should be removed?", ["Do you support or oppose the new tax?", "How many hours do you sleep on a school night?",
              "Which sport do you play most often?"], "The word \"unfair\" and \"don't you agree\" push people toward one answer."),
             ("Why is random selection important in a sample?", "It makes the sample likely to represent the population", ["It guarantees the exact answer", "It makes the sample size larger", "It removes the need for a census"],
              "Random selection avoids favoring any group, so results can be generalized.")]
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 3: margin of error
def one_moe(r):
    n = r.choice([100, 400, 625, 900, 1600, 2500, 10000, 225, 1225])
    moe = 1 / math.sqrt(n)
    kind = r.choice(["moe", "moe", "ci", "n"])
    if kind == "moe":
        q = "Estimate the margin of error for a random sample of %s people, using 1/√<i>n</i>." % num(n)
        right = "±%s%%" % ("%.1f" % (moe * 100)).rstrip("0").rstrip(".")
        return T(q, right, ["±%s%%" % ("%.1f" % (100 / n * 100)).rstrip("0").rstrip("."), "±%s%%" % ("%.1f" % (moe * 50)).rstrip("0").rstrip("."), "±%s%%" % ("%.1f" % (math.sqrt(n) / 10)).rstrip("0").rstrip(".")],
                 "1/√%s = 1/%d = %s, which is <b>%s</b>." % (num(n), round(math.sqrt(n)), ("%.4f" % moe).rstrip("0"), right))
    if kind == "ci":
        p = r.choice([42, 48, 53, 56, 61, 64, 35, 72])
        m = round(moe * 100, 1)
        mt = ("%.1f" % m).rstrip("0").rstrip(".")
        lo, hi = round(p - m, 1), round(p + m, 1)
        f = lambda v: ("%.1f" % v).rstrip("0").rstrip(".")
        q = "In a random sample of %s people, %d%% support a plan. Using a margin of error of 1/√<i>n</i>, which interval likely contains the true percent?" % (num(n), p)
        right = "%s%% to %s%%" % (f(lo), f(hi))
        return T(q, right, ["%s%% to %s%%" % (f(p - 2 * m), f(p + 2 * m)), "%d%% to %s%%" % (p, f(hi)), "%s%% to %s%%" % (f(p - 10), f(p + 10)) if m != 10 else "%s%% to %s%%" % (f(p - 5), f(p + 5))],
                 "Margin of error = 1/√%s ≈ %s%%. %d%% ± %s%% = <b>%s</b>." % (num(n), mt, p, mt, right))
    m = r.choice([2, 2.5, 4, 5, 10])
    n2 = round(1 / (m / 100) ** 2)
    q = "About how large a random sample is needed for a margin of error of ±%s%%, using 1/√<i>n</i>?" % (("%.1f" % m).rstrip("0").rstrip("."))
    return T(q, num(n2), [num(round(100 / m)), num(round(n2 / 2)), num(round(1 / (m / 100)))],
             "1/√<i>n</i> = %s, so √<i>n</i> = %s and <i>n</i> = <b>%s</b>." % (("%.3f" % (m / 100)).rstrip("0"), ("%.1f" % (100 / m)).rstrip("0").rstrip("."), num(n2)))


# ------------------------------------------------------------ set 4: interpreting results
USED_NK = set()
def one_interp(r):
    items = [("A sample size is multiplied by 4. What happens to the margin of error?", "It is cut in half", ["It is cut to one fourth", "It doubles", "It stays the same"],
              "The margin of error is about 1/√<i>n</i>, and √4 = 2."),
             ("Which sample size gives the most precise estimate?", "2,500", ["400", "900", "100"], "A larger random sample has a smaller margin of error."),
             ("A poll says 52%% ± 4%% of voters support a candidate. What can we conclude?", "The true support is likely between 48%% and 56%%, so the race is too close to call",
              ["The candidate will definitely win", "Exactly 52%% of all voters support the candidate", "The poll is useless"], "The interval includes values below 50%%."),
             ("Two polls of the same population give 45%% and 48%%, each with a margin of error of ±3%%. Are the results consistent?", "Yes, the intervals overlap",
              ["No, they must be the same", "No, one poll must be biased", "Yes, because both are below 50%%"], "42%% to 48%% and 45%% to 51%% overlap, so the difference can be due to sampling variation."),
             ("What does a margin of error describe?", "How much a sample result is likely to differ from the true population value", ["The number of mistakes in the survey", "The bias in the questions",
              "The exact error in the result"], "It describes random sampling variation, not bias."),
             ("A biased sample of 10,000 people and a random sample of 400 people both answer a survey. Which result is more trustworthy?", "The random sample of 400",
              ["The biased sample of 10,000", "They are equally trustworthy", "Neither can be used"], "A large sample does not fix bias. Random selection matters more than size."),
             ("Why do pollsters report a margin of error?", "Because different random samples give slightly different results", ["Because they made a calculation mistake", "Because the population changes every day",
              "Because only volunteers answered"], "Sample results vary from sample to sample, so an interval is more honest than one number.")]
    q, right, wr, e = r.choice(items)
    q, right, wr, e = q.replace("%%", "%"), right.replace("%%", "%"), [w.replace("%%", "%") for w in wr], e.replace("%%", "%")
    pp = People(r)
    nm, he, his = pp.next()
    if r.random() < 0.45:
        n = r.choice([100, 400, 900, 2500])
        k = r.choice([4, 9, 16, 25])
        if n * k > 40000 or (n, k) in USED_NK:
            return None
        USED_NK.add((n, k))
        m1 = 100 / math.sqrt(n)
        m2 = m1 / math.sqrt(k)
        f = lambda v: ("%.1f" % (v + 1e-9)).rstrip("0").rstrip(".")
        q = "%s surveys %s people and gets a margin of error of about ±%s%%. About what margin of error would %s get with %s people?" % (nm, num(n), f(m1), he, num(n * k))
        right = "±%s%%" % f(m2)
        return T(q, right, ["±%s%%" % f(m1 / k), "±%s%%" % f(m1 * math.sqrt(k)), "±%s%%" % f(m1)],
                 "The sample is %d times as large, so the margin of error is divided by √%d = %d: %s ÷ %d = <b>%s</b>." % (k, k, round(math.sqrt(k)), f(m1), round(math.sqrt(k)), right))
    return T(q, right, wr, e + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 5: experiments and simulation
def one_exp(r):
    kind = r.choice(["diff", "diff", "sim", "sim", "design"])
    if kind == "diff":
        a, b = r.choice([(78, 72), (85, 80), (12, 9), (6.2, 5.4), (64, 58)])
        q = "In an experiment, the treatment group's mean is %s and the control group's mean is %s. What is the difference of the means (treatment %s control)?" % (num(a), num(b), MINUS)
        d = round(a - b, 1)
        return T(q, num(d), [num(round(b - a, 1)), num(round((a + b) / 2, 1)), num(round(a + b, 1))], "%s %s %s = <b>%s</b>." % (num(a), MINUS, num(b), num(d)))
    if kind == "sim":
        p = r.choice([1, 2, 3, 4, 8, 12, 25, 40])
        q = ("The difference in an experiment was %s. In 100 random re-assignments of the same data, a difference at least that large happened %d times. "
             "What does this suggest?" % (r.choice(["6 points", "0.8 seconds", "12%"]), p))
        if p <= 5:
            right = "The difference is unlikely to be due to chance alone, so the treatment probably had an effect"
            wrong = ["The difference is likely due to chance", "The treatment definitely caused the difference in every person", "Nothing can be concluded from a simulation"]
        else:
            right = "The difference could easily be due to chance, so there is not strong evidence of an effect"
            wrong = ["The treatment certainly worked", "The difference is impossible by chance", "Nothing can be concluded from a simulation"]
        return T(q, right, wrong, "A result that happens in only about %d%% of random re-assignments is %s. <b>%s</b>." % (p, "rare (usually 5%% or less counts as significant)".replace("%%", "%") if p <= 5 else "not rare", right))
    items = [("In an experiment, why are subjects assigned to groups at random?", "To balance other factors between the groups", ["To make the groups different sizes", "To let subjects choose their treatment",
              "To avoid needing a control group"], "Random assignment spreads other variables evenly, so the treatment is the main difference."),
             ("What is a placebo?", "A fake treatment that looks like the real one", ["A second, stronger treatment", "The group that gets the real treatment", "A type of random sample"],
              "A placebo lets researchers separate the real effect from people's expectations."),
             ("In a double-blind experiment, who does not know which treatment each subject gets?", "Both the subjects and the people measuring the results", ["Only the subjects", "Only the researchers", "Nobody is kept from knowing"],
              "Double-blind keeps expectations from affecting either the subjects or the measurements."),
             ("Why should an experiment be repeated on many subjects?", "So that the results are not due to a few unusual subjects", ["To make it a survey", "To avoid using a control group", "To remove the need for randomization"],
              "Replication reduces the effect of chance variation.")]
    q, right, wr, e = r.choice(items)
    return T(q, right, wr, e + " <b>%s</b>." % right)


def build():
    sets = [S("Surveys, observational studies and experiments", collect(one_type, 20, R)),
            S("Sampling methods and bias", collect(one_samp, 20, R)),
            S("Margin of error", collect(one_moe, 20, R)),
            S("Interpreting results", collect(one_interp, 20, R)),
            S("Experiments and simulation", collect(one_exp, 20, R))]
    body = lesson(
        "<ul><li>A <b>sample survey</b> asks a sample questions. An <b>observational study</b> watches groups that already exist. "
        "An <b>experiment</b> assigns treatments, ideally at random, and is the only one of the three that can show cause and effect.</li>"
        "<li>A <b>random sample</b> represents the population. Convenience and voluntary response samples are usually <b>biased</b>.</li>"
        "<li>For a random sample of size <i>n</i>, the <b>margin of error</b> for a proportion is about 1/√<i>n</i>. The interval sample result ± margin of error likely contains the true value.</li>"
        "<li>In an experiment, a <b>simulation</b> of random re-assignments shows how often a difference happens by chance. A rare result (about 5%% or less) is evidence of a real effect.</li></ul>",
        [("A random sample of 900 people finds 58%% like a plan. Give an interval for the true percent.", ["1/√900 = 1/30 ≈ 3.3%%", "58%% ± 3.3%%"], "54.7%% to 61.3%%"),
         ("How does the margin of error change if the sample size goes from 400 to 1,600?", ["The size is 4 times as large", "√4 = 2"], "It is cut in half")],
        ["Calling an observational study an experiment. Experiments assign the treatment.",
         "Trusting a large voluntary response sample. Size does not fix bias.",
         "Thinking a larger margin of error is more precise. Smaller is more precise.",
         "Claiming that one variable causes another from an observational study."])
    body = body.replace("%%", "%")
    faq = [("What is the difference between an observational study and an experiment?", "In an experiment the researcher assigns the treatments; in an observational study the researcher only observes groups that already exist."),
           ("How do you estimate the margin of error?", "For a random sample of size n, the margin of error for a proportion is about 1/√n. For n = 400, that is 1/20 = 5%."),
           ("What makes a sample biased?", "Any method that favors some members of the population, such as asking only volunteers or only people who are easy to reach."),
           ("What does a simulation show in an experiment?", "How often a difference as large as the one observed happens by chance alone. If it is rare, the treatment likely had an effect.")]
    make("statistical-studies-and-margin-of-error", 16, "S-IC.B.4",
         "Statistical Studies, Sampling, and Margin of Error",
         "Sampling, Experiments and Margin of Error Worksheet (Algebra 2, S-IC) | 100 Questions with Answers",
         "Studies and Margin of Error",
         "Use data from a sample survey to estimate a population mean or proportion; develop a margin of error through the use of simulation models for random sampling.",
         "Free Algebra 2 worksheet on statistical studies: surveys, observational studies and experiments, sampling bias, margin of error 1/√n, confidence intervals and simulation. 100 questions.",
         "Only randomized experiments can show cause and effect.",
         "Margin of error ≈ 1/√n. Larger random samples are more precise.",
         body, faq, sets, R, domain="Statistics and Probability", grade="algebra-2")


if __name__ == "__main__":
    build()
