# -*- coding: utf-8 -*-
"""
US High School Biology: Homeostasis and Feedback (HS-LS1-3)
  python tools/gen_us_science_bio_homeostasis_and_feedback.py
Plan and conduct an investigation to provide evidence that feedback mechanisms maintain homeostasis.
Negative feedback brings a variable back to its set point: body temperature (sweating, shivering), blood glucose
(insulin, glucagon), water balance, and stomata in plants. Positive feedback pushes a change further (childbirth,
blood clotting). Reading data tables of body temperature and blood glucose.
Wrong answers come from real mistakes: "insulin raises blood sugar", "shivering cools you down", "negative feedback
means something bad".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, svg_wrap, arrow, People
from ws_common import text, INK

U = Unit(90103)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def loop_svg():
    box = lambda x, y, t: "<rect x='%d' y='%d' width='150' height='36' rx='8' fill='#eef6e8' stroke='%s' stroke-width='1.5'/>" % (x - 75, y - 18, INK) + text(x, y + 5, t, 12)
    s = box(110, 30, "body gets too hot") + box(370, 30, "brain senses it") + box(370, 120, "sweat, skin vessels widen") + box(110, 120, "body cools to 37 °C")
    s += arrow(186, 30, 294, 30, INK, 2, 7) + arrow(370, 48, 370, 102, INK, 2, 7) + arrow(294, 120, 186, 120, INK, 2, 7) + arrow(110, 102, 110, 48, INK, 2, 7)
    return svg_wrap(480, 150, s, "negative feedback loop: body too hot, brain senses it, sweating, body cools back to 37 degrees")


def g_temp():
    who = P.next()[0]
    hot = R.random() < 0.5
    t = round(R.uniform(37.6, 39.0) if hot else R.uniform(35.4, 36.5), 1)
    k = R.choice(["resp", "why"])
    if not once((t, k)):
        return None
    if k == "resp":
        a = "sweating and blood vessels in the skin widen" if hot else "shivering and blood vessels in the skin narrow"
        w = ["shivering and blood vessels in the skin narrow" if hot else "sweating and blood vessels in the skin widen", "the heart stops", "the stomach digests faster"]
        return item("%s's body temperature is %.1f °C (normal is about 37 °C). What does the body do?" % (who, t), a, w, "Negative feedback moves it back toward 37 °C.")
    a = "to lose heat and cool down" if hot else "to make heat and warm up"
    return item("%s's body temperature is %.1f °C. The body %s. Why?" % (who, t, "sweats" if hot else "shivers"), a, ["to lose heat and cool down" if not hot else "to make heat and warm up", "to make the change bigger", "to grow muscles"],
                "The response opposes the change.")


def g_sugar():
    who = P.next()[0]
    high = R.random() < 0.5
    g = R.choice([140, 150, 160, 170, 180, 190, 200]) if high else R.choice([50, 55, 60, 62, 65])
    k = R.choice(["hormone", "effect"])
    if not once((g, k)):
        return None
    if k == "hormone":
        a = "insulin" if high else "glucagon"
        return item("%s's blood glucose is %d mg/dL (normal is about 70–110). Which hormone does the pancreas release?" % (who, g), a, ["glucagon" if high else "insulin", "adrenaline only", "no hormone"],
                    "%s brings glucose %s." % (a.capitalize(), "down" if high else "up"))
    a = "Cells take in glucose and the liver stores it, so blood glucose falls." if high else "The liver releases stored glucose, so blood glucose rises."
    return item("After %s's blood glucose reaches %d mg/dL, the pancreas responds. What happens next?" % (who, g), a,
                ["The liver releases stored glucose, so blood glucose rises." if high else "Cells take in glucose and the liver stores it, so blood glucose falls.",
                 "Blood glucose keeps changing in the same direction.", "The kidneys stop working."], "Negative feedback returns it to normal.")


def g_table():
    who = P.next()[0]
    base = R.choice([90, 95, 100])
    peak = base + R.randint(50, 80)
    vals = [base, peak, base + (peak - base) // 2, base + R.randint(0, 8)]
    times = ["before lunch", "30 min after lunch", "1 hour after", "2 hours after"]
    k = R.choice(["peak", "back", "why", "rise"])
    if not once((peak, k)) or not once(("tk", k), {"peak": 4, "back": 2, "why": 2, "rise": 30}[k]):
        return None
    tab = table(["Time", "Blood glucose (mg/dL)"], [[t, str(v)] for t, v in zip(times, vals)])
    if k == "peak":
        return item(tab + "When was %s's blood glucose highest?" % who, "30 min after lunch", [t for t in times if t != "30 min after lunch"], "The biggest number is %d." % peak)
    if k == "rise":
        return item(tab + "How much did %s's blood glucose rise after lunch?" % who, "%d mg/dL" % (peak - base), ["%d mg/dL" % peak, "%d mg/dL" % (peak + base), "%d mg/dL" % (vals[2] - base)],
                    "%d − %d = %d." % (peak, base, peak - base))
    if k == "back":
        return item(tab + "What do %s's data show 2 hours after lunch?" % who, "Blood glucose returned close to normal.", ["Blood glucose kept rising.", "Blood glucose dropped to zero.", "Nothing changed all day."],
                    "That is homeostasis.")
    return item(tab + "Why did %s's blood glucose fall after 30 minutes?" % who, "Insulin helped cells take in glucose.", ["Glucagon released more glucose.", "Lunch made more sugar.", "The heart used up all the glucose."],
                "Insulin lowers blood glucose.")


LOOPS = [("Sweating when you are hot", "negative"), ("Shivering when you are cold", "negative"), ("Insulin released after a meal", "negative"),
         ("Glucagon released when blood sugar is low", "negative"), ("Drinking water when you are thirsty", "negative"), ("Stomata closing when a plant is short of water", "negative"),
         ("Breathing faster when carbon dioxide rises", "negative"), ("Contractions getting stronger during childbirth", "positive"),
         ("Platelets calling more platelets to a cut until it clots", "positive"), ("Fruit ripening faster as ripe fruit releases more ethylene", "positive")]


def g_loop():
    s, k = R.choice(LOOPS)
    if not once(s):
        return None
    a = "negative feedback (it reverses the change)" if k == "negative" else "positive feedback (it makes the change bigger)"
    return item("%s is an example of which kind of feedback?" % s, a, ["positive feedback (it makes the change bigger)" if k == "negative" else "negative feedback (it reverses the change)",
                                                                        "no feedback at all", "a mutation"], "Negative feedback keeps conditions stable.")


B1 = bank([
    ("What is homeostasis?", "keeping conditions inside the body stable", ["changing as fast as possible", "growing new cells", "digesting food"], "Steady temperature, glucose, water."),
    ("What is a set point?", "the normal value the body tries to keep", ["the highest value ever", "the time of day", "a kind of hormone"], "About 37 °C for body temperature."),
    ("What does negative feedback do?", "reverses a change to bring a value back to normal", ["makes a change bigger", "stops all body systems", "causes disease"], "It is not 'bad'."),
    ("Which organ senses body temperature?", "the brain (hypothalamus)", ["the stomach", "the kidney", "the lung"], "It acts like a thermostat."),
    ("What does insulin do?", "lowers blood glucose", ["raises blood glucose", "raises body temperature", "makes you thirsty"], "Cells take in glucose."),
    ("What does glucagon do?", "raises blood glucose", ["lowers blood glucose", "lowers body temperature", "digests fat"], "The liver releases glucose."),
    ("How does shivering help when you are cold?", "Muscle movement makes heat.", ["It cools the skin.", "It removes water.", "It lowers glucose."], "Shivering warms you."),
    ("How do plants keep from losing too much water?", "They close their stomata.", ["They open more stomata.", "They grow taller.", "They make more flowers."], "Guard cells close the pores."),
])
B5 = bank([
    ("A student exercises and measures heart rate every minute until it returns to resting. What is this investigating?", "a feedback mechanism that restores homeostasis", ["how to stop the heart", "positive feedback only", "photosynthesis"], "Measure the return to normal."),
    ("In type 1 diabetes, the pancreas makes little insulin. What happens after a meal?", "Blood glucose stays high.", ["Blood glucose drops very low.", "Body temperature falls.", "Nothing changes."], "No insulin, no lowering."),
    ("A thermostat turns the heater off when a room is warm enough. How is this like the body?", "Both use negative feedback to keep a set point.", ["Both use positive feedback.", "Neither has a set point.", "Both make glucose."], "Sensor, control, response."),
    ("A runner forgets to drink water on a hot day. How do the kidneys respond?", "They make less urine to save water.", ["They make more urine.", "They stop filtering blood.", "They make glucose."], "Water balance."),
    ("Why is a fever followed by sweating when it breaks?", "The body is cooling back down to the normal set point.", ["The body is making more heat.", "Sweat makes the fever higher.", "Sweating is random."], "Negative feedback."),
])


def body():
    think = ("<div class='qfig'>%s</div><p><b>Change → sense → respond → back to normal.</b></p>"
             "<ul><li><b>Negative feedback</b> reverses a change: too hot → sweat; too much glucose → insulin.</li>"
             "<li><b>Positive feedback</b> makes a change bigger until an event ends (childbirth, clotting).</li></ul>") % loop_svg()
    ex = [("Blood glucose is 180 mg/dL. Which hormone?", ["Too high", "Insulin lowers it"], "insulin"),
          ("Body temperature is 35.8 °C. Response?", ["Too low", "Make heat"], "shivering")]
    mist = ["Thinking insulin raises blood sugar. It lowers it.", "Thinking shivering cools you down. It makes heat.", "Thinking negative feedback means something bad. It means reversing a change."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Homeostasis", B1 + [(g_temp, 6), (g_loop, 6)]),
        ("Body temperature", [(g_temp, 14), (g_loop, 4), (g_sugar, 2)]),
        ("Blood glucose", [(g_sugar, 14), (g_table, 6)]),
        ("Reading the data", [(g_table, 12), (g_temp, 4), (g_sugar, 4)]),
        ("Feedback investigations", B5 + [(g_table, 6), (g_sugar, 4), (g_temp, 5)]),
    ])
    make("biology", "homeostasis-and-feedback", 3, "HS-LS1-3",
         "Plan and conduct an investigation to provide evidence that feedback mechanisms maintain homeostasis.",
         "Homeostasis and Feedback",
         "Homeostasis Worksheets: Negative and Positive Feedback, Insulin and Glucagon (Biology)",
         "Homeostasis",
         "Free high school biology worksheets on homeostasis (NGSS HS-LS1-3): body temperature, blood glucose, insulin and glucagon, and negative and positive feedback. 100 questions with answers.",
         "Feedback keeps the body stable.",
         "Negative feedback reverses a change and brings it back to the set point.",
         body(),
         [("What is the difference between negative and positive feedback?", "Negative feedback reverses a change (sweating cools you). Positive feedback makes a change bigger (stronger contractions in childbirth)."),
          ("How is blood glucose controlled?", "When it is high, the pancreas releases insulin to lower it. When it is low, it releases glucagon to raise it."),
          ("How can students investigate feedback?", "Measure heart rate, breathing rate or body temperature before and after exercise, then record how long they take to return to normal.")],
         sets)


if __name__ == "__main__":
    main()
