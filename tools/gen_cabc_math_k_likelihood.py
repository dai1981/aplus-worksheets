# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Likelihood (BC Mathematics Curriculum, Kindergarten Content: Likelihood of familiar life
events, using comparative language)
  python3 tools/gen_cabc_math_k_likelihood.py
Likely or unlikely everyday events, which of two events is more likely, picking from a bag without looking,
spinners, and short stories. Pictures (scenes, bags of counters, spinners) come from the BC Grade 1
likelihood unit. All numbers are 10 or less.
Wrong answers come from real mistakes: choosing what you want to happen instead of what is likely, thinking
the colour with fewer counters is more likely, and thinking a rare event can never happen.
"""
import random
from bck_common import Kids, mcq, finish, make, fig, figure, lesson, collect, S
import gen_cabc_math_g1_likelihood as g1

R = random.Random(53101)
LIK = "Likely: it happens a lot"
UNL = "Unlikely: it hardly ever happens"

# (scene, event, likely?, wrong reason)
EVENTS = [
    ("rain", "It is a November day in Vancouver. It rains.", True, "Unlikely: rain is not fun"),
    ("beach", "It snows at the beach on a hot July day.", False, "Likely: it snows in winter"),
    ("snow", "It is January in Whistler. There is snow on the mountain.", True, "Unlikely: snow is cold"),
    ("night", "It is night. You see the moon in the sky.", True, "Unlikely: the moon is far away"),
    ("school", "It is a school day. Your class reads a story.", True, "Unlikely: stories are long"),
    ("school", "It is a school day. A bear comes to class.", False, "Likely: bears live in BC"),
    ("bus", "A dog drives the school bus.", False, "Likely: dogs can ride a bus"),
    ("park", "You go to the park. You see a squirrel.", True, "Unlikely: squirrels are small"),
    ("park", "You go to the park. You see a moose on the slide.", False, "Likely: moose like parks"),
    ("ferry", "You ride the ferry. You see a seagull.", True, "Unlikely: seagulls fly fast"),
    ("ferry", "You ride the ferry. A whale jumps on the boat.", False, "Likely: whales swim near ferries"),
    ("salmon", "It is fall at a BC river. You see a salmon.", True, "Unlikely: salmon live in the sea"),
    ("cake", "It is your birthday. You get a cake with candles.", True, "Unlikely: cake is sweet"),
    ("popsicle", "A popsicle sits in the hot sun. It melts.", True, "Unlikely: popsicles are cold"),
    ("sunrise", "You wake up in the morning. The sun is up.", True, "Unlikely: it might be cloudy"),
    ("hockey", "You go to a hockey game. A player scores a goal.", True, "Unlikely: goals are hard"),
    ("egg", "You drop an egg on the floor. It bounces back up.", False, "Likely: balls bounce"),
    ("mountain", "You climb a big mountain in one minute.", False, "Likely: you are fast"),
    ("night", "You go to bed at night. You sleep.", True, "Unlikely: you want to play"),
    ("race", "A snail wins a race with a dog.", False, "Likely: snails try hard"),
    ("orca", "You visit the ocean in BC. A fish talks to you.", False, "Likely: fish swim in the ocean"),
    ("gull", "You eat lunch at the beach. A seagull comes close.", True, "Unlikely: seagulls are shy"),
]


def scene(name):
    return fig(g1.scene_svg(name))


# ------------------------------------------------------------ set 1: likely or unlikely?
def one_event(r):
    sc, ev, lik, why = r.choice(EVENTS)
    right = LIK if lik else UNL
    return mcq(scene(sc) + ev + " Is that likely or unlikely?", right, [UNL if lik else LIK, why, "We cannot tell"],
               "%s It is <b>%s</b>." % ("This happens a lot." if lik else "This hardly ever happens.", "likely" if lik else "unlikely"))


# ------------------------------------------------------------ set 2: which is more likely?
PAIRS = [("rain", "A November day in Vancouver", "It rains", "It is very hot"),
         ("snow", "A January day in Whistler", "It snows", "People swim in the lake"),
         ("beach", "A hot July day at the beach", "You build a sandcastle", "You build a snowman"),
         ("school", "A school day", "You play at recess", "A giraffe reads to the class"),
         ("park", "A walk in the park", "You see a dog", "You see a penguin"),
         ("ferry", "A ferry ride", "You see the water", "You see a camel"),
         ("salmon", "Fall at a BC river", "You see a salmon", "You see a shark"),
         ("night", "Night time", "The sky is dark", "The sun is shining"),
         ("cake", "A birthday party", "You sing a song", "You go to the dentist"),
         ("bus", "A school bus ride", "The bus stops at a stop sign", "The bus flies in the sky"),
         ("hockey", "A hockey game", "The players skate", "The players swim"),
         ("sunrise", "Breakfast time", "You eat food", "You eat a shoe")]


def one_pair(r):
    sc, when, a, b = r.choice(PAIRS)
    kind = r.choice(["more", "more", "less"])
    if kind == "more":
        return mcq(scene(sc) + "%s. Which is <b>more likely</b>?" % when, a, [b, "They are the same", "Both will never happen"],
                   "\u201c<b>%s</b>\u201d happens a lot. \u201c%s\u201d hardly ever happens." % (a, b))
    return mcq(scene(sc) + "%s. Which is <b>less likely</b>?" % when, b, [a, "They are the same", "Both will always happen"],
               "\u201c<b>%s</b>\u201d hardly ever happens. \u201c%s\u201d happens a lot." % (b, a))


# ------------------------------------------------------------ set 3: pick from a bag
COLS = ["red", "blue", "yellow", "green"]


def one_bag(r):
    c1, c2 = r.sample(COLS, 2)
    n1 = r.randint(1, 8)
    n2 = r.randint(1, 9 - n1) if n1 < 9 else 1
    if n1 == n2 or n1 + n2 > 10:
        return None
    pic = fig(g1.bag_svg([(c1, n1), (c2, n2)], r))
    big, small = (c1, c2) if n1 > n2 else (c2, c1)
    nb, ns = max(n1, n2), min(n1, n2)
    kind = r.choice(["more", "more", "less", "lik"])
    if kind == "more":
        return mcq(pic + "You pick one without looking. Which colour is <b>more likely</b>?", big, [small, "They are the same", "We cannot tell"],
                   "There are %d %s and %d %s. More %s, so <b>%s</b> is more likely." % (nb, big, ns, small, big, big))
    if kind == "less":
        return mcq(pic + "You pick one without looking. Which colour is <b>less likely</b>?", small, [big, "They are the same", "We cannot tell"],
                   "There %s only %d %s and %d %s. <b>%s</b> is less likely." % ("is" if ns == 1 else "are", ns, small, nb, big, small.capitalize()))
    if ns > 2 or nb < 4:
        return None
    return mcq(pic + "You pick one without looking. Will you get %s?" % small, "Unlikely", ["Likely", "It will happen every time", "It can never happen"],
               "There %s only %d %s and %d %s. Getting %s is <b>unlikely</b>, but it can happen." % ("is" if ns == 1 else "are", ns, small, nb, big, small))


# ------------------------------------------------------------ set 4: spinners
def one_spin(r):
    c1, c2 = r.sample(COLS, 2)
    n = r.choice([4, 6, 8])
    k = r.randint(1, n - 1)
    if k * 2 == n:
        return None
    secs = [(c1, 1)] * k + [(c2, 1)] * (n - k)
    order = secs[:]
    r.shuffle(order)
    pic = fig(g1.spinner_svg(order))
    big, small = (c1, c2) if k > n - k else (c2, c1)
    kind = r.choice(["more", "less", "lik"])
    if kind == "more":
        return mcq(pic + "You spin. Which colour is <b>more likely</b>?", big, [small, "They are the same", "We cannot tell"],
                   "%s has more parts, so <b>%s</b> is more likely." % (big.capitalize(), big))
    if kind == "less":
        return mcq(pic + "You spin. Which colour is <b>less likely</b>?", small, [big, "They are the same", "We cannot tell"],
                   "%s has fewer parts, so <b>%s</b> is less likely." % (small.capitalize(), small))
    sm = min(k, n - k)
    if sm > 1:
        return None
    return mcq(pic + "You spin. Will it land on %s?" % small, "Unlikely", ["Likely", "It will land on %s every time" % small, "It can never land on %s" % small],
               "Only 1 part is %s. Landing on %s is <b>unlikely</b>, but it can happen." % (small, small))


# ------------------------------------------------------------ set 5: stories
def one_story(r):
    K = Kids(r)
    k = K.next()
    kind = r.choice(["want", "bag", "rare", "hat", "socks"])
    if kind == "want":
        c1, c2 = r.sample(COLS, 2)
        a = r.randint(6, 9)
        b = r.randint(1, 10 - a)
        q = "A box has %d %s crayons and %d %s crayon%s. %s wants %s. %s picks one without looking. Which colour is more likely?" % (a, c1, b, c2, "" if b == 1 else "s", k["n"], c2, k["He"])
        return mcq(q, c1, [c2, "The colour %s wants" % k["he"], "They are the same"],
                   "Wanting a colour does not change the box. There are more %s crayons, so <b>%s</b> is more likely." % (c1, c1))
    if kind == "bag":
        a = r.randint(5, 8)
        q = "%s puts %d red counters and 1 blue counter in a bag. %s picks one without looking. What is likely?" % (k["n"], a, k["He"])
        return mcq(q, "%s picks red" % k["He"], ["%s picks blue" % k["He"], "%s picks green" % k["He"], "%s picks nothing" % k["He"]],
                   "There are %d red and only 1 blue, so red is likely: <b>%s picks red</b>." % (a, k["He"]))
    if kind == "rare":
        ev = r.choice([("see a rainbow", "a rainbow"), ("see an eagle", "an eagle"), ("find a sea star at the beach", "a sea star")])
        q = "%s says, “I will never %s.” Is that right?" % (k["n"], ev[0])
        return mcq(q, "No. It is unlikely, but it can happen", ["Yes. It can never happen", "Yes. It happens every day", "No. It happens every time"],
                   "Seeing %s does not happen a lot, but it can happen. <b>No. It is unlikely, but it can happen</b>." % ev[1])
    if kind == "hat":
        n = r.randint(3, 6)
        q = "The teacher puts %d names in a hat. %s's name is one of them. The teacher picks one name. Is %s likely to be picked?" % (n, k["n"], k["n"])
        return mcq(q, "Unlikely", ["Likely", "%s will be picked every time" % k["n"], "%s can never be picked" % k["n"]],
                   "There are %d names and only 1 is %s's. Getting picked is <b>unlikely</b>, but it can happen." % (n, k["n"]))
    a = r.randint(4, 8)
    q = "A drawer has %d white socks and 1 striped sock. %s takes one sock in the dark. What is more likely?" % (a, k["n"])
    return mcq(q, "A white sock", ["The striped sock", "They are the same", "No sock at all"],
               "There are %d white socks and only 1 striped sock. <b>A white sock</b> is more likely." % a)


def build():
    sets = [S("Likely or unlikely?", collect(one_event, 20, R)),
            S("Which is more likely?", collect(one_pair, 20, R)),
            S("Pick from a bag", collect(one_bag, 20, R)),
            S("Spinners", collect(one_spin, 20, R)),
            S("Likely stories", collect(one_story, 20, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li><b>Likely</b> means it happens a lot. Rain in Vancouver in November is likely.</li>"
        "<li><b>Unlikely</b> means it hardly ever happens, but it still can. Seeing a whale from the beach is unlikely.</li>"
        "<li>In a bag, the colour with <b>more</b> counters is more likely to be picked.</li>"
        "<li>On a spinner, the colour with more parts is more likely.</li></ul>",
        [figure(g1.bag_svg([("red", 6), ("blue", 2)], random.Random(5)), "6 red and 2 blue. Red is more likely. Blue is unlikely."),
         figure(g1.spinner_svg([("green", 1), ("yellow", 1), ("green", 1), ("green", 1)]), "3 green parts and 1 yellow part. Green is more likely.")],
        [["Choosing what you want to happen", "Look at what is there. Wanting does not change it."],
         ["Thinking fewer counters is more likely", "More counters of a colour means more likely."],
         ["Thinking unlikely means never", "Unlikely things can still happen, just not often."]])
    faq = [("What does likelihood mean in Kindergarten?", "Talking about how likely familiar events are, using words such as likely, unlikely, more likely and less likely."),
           ("What is the difference between unlikely and never?", "Unlikely things hardly ever happen but still can. Never means it cannot happen at all."),
           ("How can I practise at home?", "Put 6 red and 2 blue blocks in a bag and pick without looking. Talk about which colour you get more often."),
           ("Why use familiar life events?", "Children already know about rain, school days and birthdays, so they can judge what happens a lot and what hardly ever happens.")]
    make("likelihood", 11, "Data and probability", "Likelihood: Likely and Unlikely", "Likelihood",
         "Likelihood of familiar life events, using comparative language: using comparative language to describe likelihood (e.g., more likely, less likely, likely, unlikely)",
         "Free Kindergarten math worksheets on likelihood for the BC curriculum: likely and unlikely events, which is more likely, picking from a bag, spinners and stories. 100 picture questions with answers.",
         "Likely means it happens a lot. Unlikely means it hardly ever happens.", "More counters or more parts of a colour make it more likely.",
         body, faq, sets)


if __name__ == "__main__":
    build()
