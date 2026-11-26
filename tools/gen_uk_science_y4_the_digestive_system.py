# -*- coding: utf-8 -*-
"""
UK Year 4 science: The Digestive System (Animals, including humans)
  python tools/gen_uk_science_y4_the_digestive_system.py
The basic parts of the digestive system (mouth, oesophagus, stomach, small and large intestines, rectum) and their
jobs, the order food passes through, how long food spends in each part, and simple models of digestion.
Reuses the organ and order questions of the Year 6 unit (new seed) and adds Year 4 questions.
Wrong answers come from real mistakes: "food goes down the windpipe", "digestion happens only in the stomach",
"the large intestine is longer than the small intestine".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq
import gen_uk_science_y6_transporting_nutrients_and_water as T

T.U = Unit(61404)
T.R = T.U.R
T.P = People(T.R)
uk_sci.USED.clear()
U, R, P = T.U, T.R, T.P

TIME = [("the mouth", "about 1 minute"), ("the oesophagus", "about 10 seconds"), ("the stomach", "a few hours"), ("the large intestine", "about a day or more")]


def g_time():
    o, t = R.choice(TIME)
    if not once(("ti", o)):
        return None
    return item("Roughly how long does food stay in %s?" % o, t, [x[1] for x in TIME if x[1] != t],
                "Food moves quickly down the oesophagus but stays for hours in the stomach and intestines.")


def g_sum():
    who = P.next()[0]
    a = R.choice([2, 3, 4])
    b = R.choice([3, 4, 5, 6])
    c = R.choice([12, 16, 18, 20, 24])
    if not once(("su", a, b, c)):
        return None
    t = a + b + c
    g = "%d hours" % t
    tab = table(["Part", "Time food stays there (hours)"], [["stomach", str(a)], ["small intestine", str(b)], ["large intestine", str(c)]])
    return item(tab + "%s's book gives these times. About how long is food in these three parts altogether?" % who, g, uniq(g, ["%d hours" % c, "%d hours" % (a + b), "%d hours" % (t + 10), "%d hours" % (a * b)]),
                "%d + %d + %d = %d hours." % (a, b, c, t))


MODEL = [("Mashing bread and banana in a sandwich bag with your hands", "the stomach churning food"), ("Adding orange juice to the mashed food", "acid in the stomach"),
         ("Squeezing the mixture through a pair of tights", "nutrients passing through the small intestine walls"),
         ("Cutting food into small pieces with scissors", "teeth chewing food in the mouth"), ("Adding water to the bag", "saliva making food soft"),
         ("Squeezing the leftover mush out of the end of the tights", "waste leaving the body")]


def g_model():
    a, b = R.choice(MODEL)
    if not once(("mo", a)):
        return None
    return item("In a model of the digestive system, what does this step show? %s." % a, b, R.sample([x[1] for x in MODEL if x[1] != b], 3), "Models help us picture what happens inside the body.")


B1 = bank([
    ("What is the job of the digestive system?", "to break food down so the body can use it", ["to pump blood", "to help us breathe", "to hold up the body"], "Digestion."),
    ("Which tube does food travel down from the mouth to the stomach?", "the oesophagus", ["the windpipe", "a vein", "the small intestine"], "The windpipe carries air."),
    ("Which part of the digestive system is the longest?", "the small intestine", ["the stomach", "the large intestine", "the oesophagus"], "About 6 to 7 m in an adult."),
    ("What does the stomach use to break down food?", "acid, digestive juices and squeezing muscles", ["teeth", "air", "bones"], "It churns food into a thick liquid."),
    ("Where do nutrients pass into the blood?", "the small intestine", ["the mouth", "the rectum", "the oesophagus"], "Through its thin walls."),
    ("What does the large intestine take back from waste?", "water", ["blood", "air", "teeth"], "It makes waste more solid."),
    ("What is saliva?", "a liquid in the mouth that makes food soft and starts to digest it", ["a type of tooth", "stomach acid", "a muscle"], "Made by glands in the mouth."),
    ("Where is waste stored before it leaves the body?", "the rectum", ["the stomach", "the mouth", "the oesophagus"], "At the end of the large intestine."),
])
B5 = bank([
    ("Why is it important to chew food well?", "Smaller pieces are easier to swallow and digest.", ["It makes food heavier.", "It stops digestion.", "Teeth need the exercise only."], "Start of digestion."),
    ("Why does food still reach your stomach if you eat while upside down?", "Muscles in the oesophagus squeeze food along.", ["Gravity pulls it up.", "It does not reach the stomach.", "The stomach sucks it in."], "Muscle squeezing."),
    ("Why is fibre important for the digestive system?", "It helps food move through the intestines.", ["It is absorbed into the blood.", "It makes teeth sharp.", "It stops the stomach working."], "Keeps things moving."),
    ("In a digestive system model, what could you use to show the small intestine?", "a pair of tights, because nutrients can pass through", ["a plastic bag with no holes", "a pair of scissors", "a funnel only"], "Choose a model with holes."),
    ("Why should you wash your hands before eating?", "to stop germs getting into your digestive system", ["to make food taste better", "to help chewing", "to warm your hands"], "Hygiene."),
])


def body():
    think = ("<p><b>The digestive system breaks food down so the body can use it.</b></p>"
             "<ul><li>Mouth (teeth chew, saliva softens) → oesophagus → stomach (acid and churning) → small intestine (nutrients into the blood) → large intestine (water taken back) → rectum.</li>"
             "<li>Food passes quickly down the oesophagus but stays for hours in the stomach and intestines.</li></ul>")
    ex = [("Food leaves the stomach. Where next?", ["Stomach → small intestine"], "the small intestine"),
          ("Stomach 3 h, small intestine 4 h, large intestine 20 h. Total?", ["3 + 4 + 20"], "27 hours")]
    mist = ["Thinking food goes down the windpipe.", "Thinking digestion only happens in the stomach.", "Thinking the large intestine is the longest part."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of the digestive system", B1 + [(T.g_org, 12)]),
        ("The journey of food", [(T.g_next, 10), (g_time, 4), (g_model, 6)]),
        ("How long it takes", [(g_sum, 15), (T.g_loss, 5)]),
        ("Water in and out", [(T.g_drink, 14), (T.g_loss, 6)]),
        ("Thinking about digestion", B5 + [(g_sum, 8), (T.g_drink, 7)]),
    ])
    make_uk(4, "the-digestive-system", 4, "Animals, including humans",
            "Describe the simple functions of the basic parts of the digestive system in humans.",
            "The Digestive System",
            "Year 4 Science: The Digestive System Worksheets (Mouth, Stomach and Intestines)",
            "Digestive System",
            "Free Year 4 science worksheets on the digestive system: the mouth, oesophagus, stomach, small and large intestines and rectum, the journey of food, and digestion models. 100 questions with answers.",
            "Food is broken down on a long journey.",
            "Mouth, oesophagus, stomach, small intestine, large intestine, rectum.",
            body(),
            [("What are the parts of the digestive system?", "The mouth, oesophagus, stomach, small intestine, large intestine and rectum. Each has its own job in breaking down food."),
             ("What does the small intestine do?", "It finishes digesting food, and nutrients pass through its thin walls into the blood."),
             ("How long does digestion take?", "Usually between one and three days from eating to waste leaving the body, with most of the time spent in the intestines.")],
            sets)


if __name__ == "__main__":
    main()
