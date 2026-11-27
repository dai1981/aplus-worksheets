# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Physics (6091), Topic 13: Static Electricity
  python tools/gen_sg_science_s4_static_electricity.py
Positive and negative charge (coulomb); like charges repel and unlike charges attract; charging by friction (transfer of
electrons); conductors and insulators; charging by induction and earthing; electric fields and field-line patterns; hazards
(lightning, sparks when refuelling) and uses (electrostatic precipitators, spray painting, photocopiers).
US and UK static-electricity makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "positive charges move when a rod is rubbed", "a neutral object has no charges",
"field lines point from negative to positive", "only like charges exert forces".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 4, "Physics", 1
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

us_sign = src("gen_us_science_phys_electric_force_and_coulombs_law", "g_sign")
uk_static = src("gen_uk_science_y8_electricity", "g_static")
us_force = keep(src("gen_us_science_phys_electric_and_magnetic_fields", "g_force"), lambda it: "field pointing" in it["q"])

RUB = [("a polythene rod", "a woollen cloth", "negative", "electrons move from the cloth to the rod"),
       ("an acetate rod", "a woollen cloth", "positive", "electrons move from the rod to the cloth"),
       ("a perspex rod", "a woollen cloth", "positive", "electrons move from the rod to the cloth"),
       ("a balloon", "your hair", "negative", "electrons move from your hair to the balloon"),
       ("an ebonite rod", "fur", "negative", "electrons move from the fur to the rod"),
       ("a glass rod", "a silk cloth", "positive", "electrons move from the rod to the silk")]


def g_rub():
    a, b, ch, how = R.choice(RUB)
    k = R.choice(["rod", "cloth", "how"])
    other = "positive" if ch == "negative" else "negative"
    if k == "rod":
        return tq("%s is rubbed with %s and becomes %sly charged. Why?" % (a[0].upper() + a[1:], b, ch), how[0].upper() + how[1:] + ".",
                  ["Protons move from the %s to the %s." % (b.split()[-1], a.split()[-1]) if ch == "negative" else "Protons move from the %s to the %s." % (a.split()[-1], b.split()[-1]),
                   "Positive charges are made by friction.", "Electrons are destroyed by rubbing."], "Only electrons move when objects are rubbed; protons stay in the nuclei.")
    if k == "cloth":
        return tq("%s is rubbed with %s and becomes %sly charged. What charge does %s gain?" % (a[0].upper() + a[1:], b, ch, b.replace("a ", "the ").replace("your ", "your ")), "an equal %s charge" % other,
                  ["an equal %s charge" % ch, "no charge", "a larger %s charge" % other], "Charge is transferred, not created: the two objects get equal and opposite charges.")
    return tq("What moves when %s is charged by rubbing it with %s?" % (a, b), "electrons", ["protons", "neutrons", "positive ions in the rod"], "Electrons are transferred by friction.")


def g_force2():
    pairs = [("a positively charged rod", "a positively charged rod", "They repel."), ("a negatively charged rod", "a negatively charged rod", "They repel."),
             ("a positively charged rod", "a negatively charged rod", "They attract."), ("a negatively charged rod", "a neutral piece of paper", "They attract."),
             ("a positively charged rod", "a neutral piece of paper", "They attract."), ("a negatively charged balloon", "a positively charged balloon", "They attract."),
             ("a positively charged balloon", "a positively charged balloon", "They repel."), ("a negatively charged comb", "a thin stream of tap water", "They attract.")]
    a, b, ans = R.choice(pairs)
    return tq("%s is brought near %s. What happens?" % (a[0].upper() + a[1:], b), ans, [x for x in ("They repel.", "They attract.", "Nothing happens.", "Both lose all their charge at once.") if x != ans],
              "Like charges repel, unlike charges attract, and a charged object attracts a neutral one by induction.")


def g_chain():
    n = R.choice([1, 2, 3])
    names = ["P", "Q", "R", "S"][:n + 1]
    last = R.choice(["positive", "negative"])
    parts = ["%s repels %s" % (names[i], names[i + 1]) for i in range(n)]
    if R.random() < 0.5:
        q = "Charged spheres: %s. %s is %s. What is the charge on %s?" % (", ".join(parts), names[-1], last, names[0])
        return tq(q, last, ["positive" if last == "negative" else "negative", "neutral", "it cannot be known"], "Repulsion only happens between like charges, so every sphere in the chain has the same charge.")
    other = "positive" if last == "negative" else "negative"
    q = "%s attracts %s. %s is %s. What can %s be?" % (names[0], names[-1], names[-1], last, names[0]) if n == 1 else \
        "%s. %s attracts a sphere T. %s is %s. What can T be?" % (", ".join(parts), names[0], names[-1], last)
    return tq(q[0].upper() + q[1:], "%s or neutral" % other, [last, "%s only" % other, "neutral only"],
              "Attraction happens between unlike charges, and also between a charged object and a neutral one (by induction).")


IND = [("A negatively charged rod is held near a neutral metal sphere on an insulating stand. What happens to the electrons in the sphere?", "They are repelled to the far side of the sphere.",
        ["They are attracted to the near side.", "They leave the sphere.", "They do not move."]),
       ("A negatively charged rod is held near a metal sphere, which is then earthed with a finger. What happens?", "Electrons flow from the sphere to earth.",
        ["Electrons flow from earth to the sphere.", "Protons flow to earth.", "Nothing flows."]),
       ("A negatively charged rod is held near a metal sphere. The sphere is earthed, the earth is removed, and then the rod is taken away. What charge is left on the sphere?", "positive",
        ["negative", "no charge", "it depends on the size of the sphere"]),
       ("A positively charged rod is held near a metal sphere. The sphere is earthed, the earth is removed, and then the rod is taken away. What charge is left on the sphere?", "negative",
        ["positive", "no charge", "positive on one side only"]),
       ("A positively charged rod is held near an earthed metal sphere. Which way do electrons flow?", "from earth onto the sphere", ["from the sphere to earth", "from the rod to the sphere", "no electrons flow"]),
       ("Why must the earth connection be removed before the charged rod is taken away when charging by induction?", "Otherwise the charge would flow back and the sphere would become neutral.",
        ["Otherwise the rod would lose its charge.", "Otherwise the sphere would become too hot.", "It makes no difference."])]


def g_ind():
    q, a, w = R.choice(IND)
    return tq(q, a, w, "In charging by induction, a nearby charged object pushes or pulls electrons; earthing lets electrons flow; the sphere ends with the opposite charge to the rod.")


CI = [("copper", "conductor"), ("aluminium", "conductor"), ("graphite", "conductor"), ("the human body", "conductor"), ("salt water", "conductor"), ("steel", "conductor"),
      ("rubber", "insulator"), ("glass", "insulator"), ("dry wood", "insulator"), ("polythene", "insulator"), ("nylon", "insulator"), ("dry air", "insulator")]


def g_ci():
    m, a = R.choice(CI)
    return tq("Is %s an electrical conductor or an insulator?" % m, "a conductor" if a == "conductor" else "an insulator",
              ["an insulator" if a == "conductor" else "a conductor", "neither: it can never be charged", "a magnet"],
              "Conductors have charges (such as free electrons) that can move; insulators hold charges in place, so they can be charged by rubbing.")


FIELD = [("What is an electric field?", "a region in which an electric charge experiences an electric force", ["a region where a magnet feels a force", "the path a current takes", "a region with no charges"]),
         ("Which way do electric field lines point?", "from positive charges towards negative charges", ["from negative to positive", "around in circles", "towards both charges"]),
         ("What do electric field lines show?", "the direction of the force on a small positive charge placed in the field", ["the path of electrons only", "the direction of a magnetic force", "where charges are stored"]),
         ("What do closely spaced field lines show?", "a stronger electric field", ["a weaker electric field", "no field", "a magnetic field"]),
         ("Describe the field between two parallel plates, one positive and one negative.", "uniform: straight, parallel, evenly spaced lines from the positive plate to the negative plate",
          ["curved lines from the negative plate to the positive plate", "circles around each plate", "no field between the plates"]),
         ("Describe the field around an isolated positive point charge.", "straight lines pointing radially outwards", ["straight lines pointing radially inwards", "circles around the charge", "parallel lines"]),
         ("Describe the field around an isolated negative point charge.", "straight lines pointing radially inwards", ["straight lines pointing radially outwards", "circles around the charge", "parallel lines"])]


def g_field():
    q, a, w = R.choice(FIELD)
    return tq(q, a, w, "Field lines go from + to −; their spacing shows the strength of the field.")


POOL1 = pool(R, [
    ("What is the SI unit of electric charge?", "the coulomb (C)", ["the ampere (A)", "the volt (V)", "the ohm (Ω)"], "Charge Q is measured in coulombs."),
    ("What is the charge on an electron?", "negative", ["positive", "zero", "it changes when rubbed"], "Protons are positive; neutrons have no charge."),
    ("Why does a neutral object have no overall charge?", "It has equal numbers of protons and electrons.", ["It has no charged particles.", "It has only neutrons.", "Its charges have been destroyed."], "The charges cancel."),
    ("Why can a metal rod held in your hand not be charged by rubbing?", "Charge flows through the metal and your body to earth.", ["Metals have no electrons.", "Metals cannot be rubbed.", "Metals only take positive charge."], "Metals and the body are conductors."),
    ("A charged balloon sticks to a wall. Why?", "It induces an opposite charge on the wall's surface, which attracts it.", ["The wall is magnetic.", "Air pressure pushes it.", "The wall is always positively charged."], "Attraction by induction."),
    ("Why do you sometimes get a small shock when touching a metal door handle after walking on a carpet?", "Your body has gained charge, which flows to earth through the handle as a spark.",
     ["The handle is live.", "The carpet is magnetic.", "Friction heats the handle."], "Charge builds up by friction."),
    ("What is earthing?", "connecting an object to the ground with a conductor so that charge can flow away", ["covering an object with soil", "giving an object a positive charge", "insulating an object from the ground"], "It removes excess charge."),
    ("Which particle carries the negative charge in an atom?", "the electron", ["the proton", "the neutron", "the nucleus"], "Electrons orbit the positive nucleus."),
    ("A charged rod attracts a small piece of paper. Can you tell the charge on the rod from this?", "No, a rod with either charge attracts neutral paper by induction.", ["Yes, it must be positive.", "Yes, it must be negative.", "Yes, the paper must be charged."], "Only repulsion proves a charge."),
    ("Which is the only sure test that an object is charged?", "It repels an object with a known charge.", ["It attracts paper.", "It feels warm.", "It is shiny."], "Neutral objects can be attracted but never repelled."),
    ("Two charged spheres repel each other. What can you say about their charges?", "They have the same sign (both positive or both negative).", ["They have opposite signs.", "One must be neutral.", "They must both be negative."], "Like charges repel."),
])
POOL5 = pool(R, [
    ("Why is a fuel tanker connected to the ground with a cable before refuelling an aircraft?", "Charge that builds up by friction flows safely to earth, so no spark ignites the fuel vapour.",
     ["To stop the fuel leaking.", "To keep the fuel cool.", "To measure the fuel."], "A spark near fuel vapour could cause an explosion."),
    ("How does a lightning conductor protect a tall building?", "It gives the charge a low-resistance path to earth, so it does not pass through the building.", ["It attracts all lightning away from Singapore.", "It stores the charge.", "It makes the building insulating."], "A thick copper strip runs down to the ground."),
    ("How do electrostatic precipitators clean smoke in factory chimneys?", "Smoke particles are charged and then attracted to oppositely charged plates.", ["The smoke is cooled into water.", "Magnets pull out the dust.", "The smoke is burned again."], "The collected dust is removed later."),
    ("Why is a car charged before it is spray-painted?", "The paint droplets are given the opposite charge, so they are attracted evenly to the car and less paint is wasted.",
     ["To dry the paint faster.", "To make the paint shiny.", "To stop the paint sticking."], "Like-charged droplets also spread out evenly."),
    ("In a photocopier, why does the black toner powder stick only to parts of the drum?", "Light removes the charge where the page is white, so toner is attracted only to the charged dark areas.",
     ["The toner is magnetic.", "Heat makes it stick.", "The drum is sticky."], "Charged areas form an image of the page."),
    ("Why is it dangerous to stand under a tall tree during a thunderstorm?", "Lightning often strikes tall objects and the charge may pass through you to the ground.", ["The tree attracts rain.", "Leaves conduct electricity well.", "It is not dangerous."], "Crouch low in an open area away from trees."),
    ("A polythene rod rubbed with a cloth repels a charged balloon. The balloon was charged by rubbing on hair. What are their charges?", "both negative", ["both positive", "rod positive, balloon negative", "rod negative, balloon positive"], "Polythene becomes negative; like charges repel."),
    ("Why is it hard to charge objects by rubbing on a humid day in Singapore?", "Moist air and a film of water on surfaces let the charge leak away.", ["Humid air is an insulator.", "Electrons stop moving in humid air.", "Rubbing creates protons instead."], "Damp air conducts slightly."),
    ("Why do aircraft tyres contain conducting material?", "So charge built up during flight can flow to earth when the plane lands.", ["To make them stronger.", "To keep them cool.", "To make them lighter."], "Prevents sparks during refuelling."),
    ("A negatively charged sphere is earthed. What happens?", "Electrons flow from the sphere to earth until it is neutral.", ["Protons flow from earth to the sphere.", "Electrons flow from earth to the sphere.", "Nothing happens."], "Excess electrons leave."),
])


def main():
    sets = U.sets([
        ("Charges and forces", [(POOL1, 6), (g_force2, 5), (g_chain, 4), (us_sign, 5)]),
        ("Charging by friction", [(g_rub, 10), (uk_static, 4), (g_ci, 6)]),
        ("Charging by induction", [(g_ind, 6), (POOL1, 5), (us_sign, 5), (g_rub, 4)]),
        ("Electric fields", [(g_field, 7), (us_force, 6), (g_ci, 4), (us_sign, 3)]),
        ("Hazards, uses and exam-style questions", [(POOL5, 10), (g_chain, 6), (g_force2, 3), (uk_static, 2)]),
    ])
    make_ol(LV, SUBJ, "static-electricity", SORT, "Static Electricity",
            "State that there are positive and negative charges and that charge is measured in coulombs; state that unlike charges attract and like charges repel; "
            "explain electrostatic charging by friction in terms of the transfer of electrons; distinguish between electrical conductors and insulators; describe "
            "charging by induction and the role of earthing; describe an electric field as a region in which a charge experiences a force and draw field-line patterns "
            "for point charges and parallel plates; describe hazards and applications of static electricity (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Static Electricity", "Static electricity",
            "Free Secondary 4 O-Level Physics worksheets on static electricity: positive and negative charge, charging by friction and induction, earthing, electric fields, "
            "hazards and uses. 100 questions with answers.",
            "Like charges repel; unlike charges attract.", "Only electrons move when objects are charged by rubbing.",
            "<p><b>Objects become charged when electrons are transferred.</b></p><ul>"
            "<li>Rubbing moves electrons from one object to the other: the one that gains electrons becomes negative, the other positive by an equal amount.</li>"
            "<li>Like charges repel; unlike charges attract; a charged object attracts a neutral one by induction.</li>"
            "<li>Charging by induction: bring a charged rod near, earth the conductor, remove the earth, then remove the rod. The conductor gets the opposite charge.</li>"
            "<li>Electric field lines point from + to −. Earthing and lightning conductors let charge flow safely to the ground.</li></ul>",
            [("A polythene rod rubbed with wool becomes negative. What happened?", ["electrons moved from the wool to the rod"], "the wool becomes positive"),
             ("A positive rod is held near a sphere that is earthed, then earth removed, then rod removed. Charge?", ["electrons flow up from earth", "they stay when earth is removed"], "negative")],
            ["Saying positive charges move when objects are rubbed. Only electrons move.", "Thinking a neutral object has no charges. It has equal + and −.",
             "Drawing field lines from − to +. They go from + to −.", "Removing the rod before the earth connection in charging by induction."],
            [("How does charging by friction work?", "Rubbing two insulators together transfers electrons from one to the other. The object that gains electrons becomes negative and the other becomes positive."),
             ("What is charging by induction?", "Charging a conductor without touching it: a nearby charged object moves its electrons, earthing lets electrons flow in or out, and the conductor is left with the opposite charge."),
             ("Why is static electricity dangerous when refuelling?", "Friction can build up charge, and a spark could ignite fuel vapour, so vehicles and aircraft are earthed first.")],
            sets)


if __name__ == "__main__":
    main()
