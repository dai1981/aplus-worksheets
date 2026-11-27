# -*- coding: utf-8 -*-
"""
Singapore Primary 3 science: Magnets (Interactions)
  python tools/gen_sg_science_p3_magnets.py
Magnets attract magnetic materials (iron, steel, nickel, cobalt); every magnet has a north and a south pole;
like poles repel and unlike poles attract; a freely hanging magnet points north-south.
Making a magnet: stroking a steel object in one direction with one pole (stroke method) and the electrical method
(a coil of wire around an iron nail connected to a battery); uses of magnets in daily life.
UK Year 3 magnet questions are reused with Singapore names; making magnets and PSLE-style tests are written here.
Wrong answers come from real mistakes: "all metals are magnetic", "a magnet attracts aluminium cans",
"stroking back and forth makes a strong magnet", "the bigger the magnet, the stronger it is".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63306)
R = U.R
P = People(R)
AR = use(U, "gen_uk_science_y3_magnets_attract_and_repel")
MM = use(U, "gen_uk_science_y3_magnetic_materials")


def g_coil():
    turns = [10, 20, 30, 40]
    clips = [R.randint(2, 4)]
    for _ in range(3):
        clips.append(clips[-1] + R.randint(2, 5))
    k = R.choice(["trend", "most", "var", "same", "pred", "off", "read"])
    if not once(("cl", k), 2 if k in ("most", "read") else 1):
        return None
    tb = table(["Number of coils of wire", "Number of paper clips picked up"], [[str(t), str(c)] for t, c in zip(turns, clips)])
    q0 = "%s wound wire around an iron nail and connected it to a battery. She changed the number of coils.<br>%s" % (P.next()[0], tb)
    if k == "trend":
        return item(q0 + "What does the table show?", "The more coils of wire, the stronger the magnet.",
                    ["The fewer coils, the stronger the magnet.", "The number of coils makes no difference.", "The nail is not a magnet."],
                    "More coils make a stronger electromagnet.")
    if k == "most":
        return item(q0 + "How many paper clips did the nail pick up with 30 coils?", str(clips[2]), [str(c) for c in (clips[1], clips[3], clips[2] + 10)],
                    "Read the row for 30 coils.")
    if k == "read":
        return item(q0 + "How many more paper clips were picked up with 40 coils than with 10 coils?", str(clips[3] - clips[0]),
                    [str(clips[3]), str(clips[0]), str(clips[3] + clips[0])], "%d − %d = %d." % (clips[3], clips[0], clips[3] - clips[0]))
    if k == "var":
        return item(q0 + "What was changed in this experiment?", "the number of coils of wire", ["the number of paper clips", "the type of nail", "the number of batteries"],
                    "Only the number of coils was changed; the number of paper clips was measured.")
    if k == "same":
        return item(q0 + "Which should be kept the same for a fair test?", "the number of batteries and the size of the nail",
                    ["the number of coils", "the number of paper clips picked up", "the time of day only"], "Only the number of coils should change.")
    if k == "pred":
        return item(q0 + "Predict how many paper clips 50 coils would pick up.", "more than %d" % clips[3], ["fewer than %d" % clips[0], "exactly %d" % clips[0], "none"],
                    "The pattern shows more coils pick up more paper clips.")
    return item(q0 + "What happens to the paper clips when the battery is disconnected?", "Most of them drop off.",
                ["More paper clips are picked up.", "They stick for ever.", "They turn into magnets for ever."],
                "An electromagnet works only when electric current flows.")


def g_through():
    mats = ["paper", "plastic", "glass", "wood", "cloth"]
    m = R.choice(mats)
    k = R.choice(["yes", "steel"])
    if not once(("th", k, m if k == "yes" else "")):
        return None
    if k == "yes":
        return item("A magnet is held above a sheet of %s with a steel paper clip on the other side. What happens?" % m,
                    "The paper clip is still attracted through the %s." % m, ["The paper clip is repelled.", "Nothing happens at all.", "The %s becomes a magnet." % m],
                    "Magnetic force can act through non-magnetic materials such as %s." % m)
    return item("A magnet is held above a thick steel plate with a paper clip under it. Why is the paper clip attracted less?",
                "The steel plate is attracted and takes up much of the magnetic force.", ["Steel is not magnetic.", "The paper clip is too heavy.", "The magnet is repelled."],
                "Magnetic materials such as steel can block some of the magnetic force.")


B1 = bank([
    ("What are the two ends of a magnet called?", "the north pole and the south pole", ["the top and the bottom", "the plus and the minus", "the head and the tail"], "The magnetic force is strongest at the poles."),
    ("Where is the magnetic force of a bar magnet strongest?", "at the poles", ["in the middle", "it is the same everywhere", "on the label"], "More paper clips stick to the ends."),
    ("Which of these materials is attracted to a magnet?", "iron", ["copper", "aluminium", "plastic"], "Iron, steel, nickel and cobalt are magnetic materials."),
    ("Which statement is correct?", "Like poles repel and unlike poles attract.", ["Like poles attract and unlike poles repel.", "All poles attract.", "All poles repel."], "N and N repel; N and S attract."),
    ("A bar magnet hangs freely from a string. Which way does it come to rest?", "pointing north and south", ["pointing east and west", "pointing up and down", "it keeps spinning"], "A freely hanging magnet points north-south."),
    ("Which of these is a non-magnetic material?", "wood", ["steel", "nickel", "iron"], "Wood is not attracted to a magnet."),
    ("What is the surest way to find out if an object is a magnet?", "Check whether it repels one pole of a known magnet.", ["Check whether it attracts a magnet.", "Check whether it is heavy.", "Check whether it is shiny."], "Only a magnet can repel a magnet. A plain steel object attracts both poles."),
    ("Can a magnet attract an object without touching it?", "Yes. The magnetic force acts over a distance.", ["No, it must touch.", "Only underwater.", "Only in the dark."], "A paper clip jumps to a magnet before they touch."),
])
B2 = bank([
    ("How do you make a magnet by the stroke method?", "Stroke a steel needle many times in one direction with one pole of a magnet.", ["Rub the needle back and forth with any end.", "Heat the needle.", "Drop the needle many times."], "Stroking in one direction with the same pole makes the needle a magnet."),
    ("Why must you lift the magnet away at the end of each stroke?", "so that you stroke in the same direction every time", ["to cool the magnet", "to make the needle heavier", "to break the needle"], "Stroking back and forth does not make a good magnet."),
    ("Which object can be made into a magnet by stroking?", "a steel screwdriver", ["a copper wire", "a plastic ruler", "an aluminium can"], "Only magnetic materials can be made into magnets."),
    ("What is the electrical method of making a magnet?", "winding a coil of wire around an iron nail and connecting it to a battery", ["putting a nail in water", "painting a nail red", "hitting a nail with a hammer"], "This makes an electromagnet."),
    ("How can you make an electromagnet stronger?", "Add more coils of wire or use more batteries.", ["Use a plastic rod instead of an iron nail.", "Use fewer coils.", "Disconnect the battery."], "More coils or more batteries give a stronger magnet."),
    ("What is the main advantage of an electromagnet?", "It can be switched on and off.", ["It works without electricity.", "It never gets weaker.", "It attracts aluminium."], "Cranes in scrapyards switch electromagnets off to drop the metal."),
    ("A magnet made by stroking can lose its magnetism. Which action would make this happen?", "dropping it many times or heating it", ["keeping it in a box", "stroking it again in one direction", "putting it near paper"], "Rough handling and heat can weaken magnets."),
    ("Why does an iron nail stop being a magnet when the battery is disconnected?", "There is no electric current to make it magnetic.", ["The nail melts.", "The coils fall off.", "The nail becomes copper."], "An electromagnet needs electric current."),
])
B3 = bank([
    ("How does a magnetic door catch work?", "A magnet in the frame attracts a steel plate on the door.", ["The door is pushed by the wind.", "The magnet repels the door.", "The door is glued."], "This keeps cupboard doors closed."),
    ("How are magnets used at recycling centres?", "to separate steel cans from aluminium cans", ["to melt the cans", "to clean the cans", "to crush the cans"], "Steel cans are attracted; aluminium cans are not."),
    ("Why is a compass useful when hiking in a forest?", "Its magnetic needle points north, so you can find your direction.", ["It lights up the path.", "It tells the time.", "It attracts water."], "The needle is a small magnet."),
    ("How are magnets used in some toys, such as fishing games?", "Magnets on the rods attract the steel parts on the toy fish.", ["The fish are made of plastic only.", "The rods repel the fish.", "The fish float up by themselves."], "The steel parts are attracted to the magnets."),
    ("Which of these uses an electromagnet?", "an electric doorbell", ["a fridge magnet", "a compass needle", "a magnetic bookmark"], "Doorbells and cranes use electromagnets that switch on and off."),
    ("How do magnets help to keep things neat in a toolbox?", "A magnetic strip holds steel tools in place.", ["Magnets make tools lighter.", "Magnets clean the tools.", "Magnets repel the tools."], "Steel tools are attracted to the strip."),
    ("What keeps a fridge door shut tightly?", "magnetic strips in the rubber seal", ["glue", "a spring only", "air pressure only"], "The magnets attract the steel body of the fridge."),
])
B5 = bank([
    ("Siti wants to find out which of three magnets is the strongest. Which is the best method?", "Count how many paper clips each magnet can hold in a chain.", ["Weigh each magnet.", "Measure the length of each magnet.", "Look at the colour of each magnet."], "A stronger magnet holds more paper clips."),
    ("A big magnet held fewer paper clips than a small magnet. What does this show?", "The size of a magnet does not always tell how strong it is.", ["Big magnets are always weaker.", "The paper clips are not magnetic.", "The small magnet is not a magnet."], "Test the strength; do not judge by size."),
    ("Ravi stroked a steel needle 10 times, 20 times and 30 times. Each time he counted the pins it picked up. What was he testing?", "how the number of strokes affects the strength of the magnet made", ["whether pins are magnetic", "whether needles are made of steel", "how heavy the pins are"], "Only the number of strokes was changed."),
    ("A pupil moved a magnet closer and closer to a paper clip on a table. She measured the distance when the clip first moved. What is she finding out?", "how strong the magnet is", ["whether the clip is made of plastic", "how heavy the table is", "whether the magnet is shiny"], "A stronger magnet attracts the clip from further away."),
    ("Mei Ling put a paper clip in a glass of water and moved a magnet outside the glass. The clip moved. What does this show?", "Magnetic force can act through glass and water.", ["Water is magnetic.", "Glass is magnetic.", "The clip is a magnet."], "Glass and water are non-magnetic, so the force passes through them."),
    ("Two ring magnets on a pencil float one above the other with a gap. Why?", "Like poles are facing each other, so they repel.", ["Unlike poles are facing, so they attract.", "The pencil is magnetic.", "The magnets have lost their magnetism."], "Repulsion holds the top magnet up."),
    ("A steel bar attracted both ends of a magnet. What can you conclude?", "The steel bar is not a magnet.", ["The steel bar is a strong magnet.", "The steel bar is made of copper.", "The magnet is broken."], "A magnet would repel one pole."),
])


def body():
    think = ("<p><b>A magnet attracts magnetic materials: iron, steel, nickel and cobalt.</b></p>"
             "<ul><li>Every magnet has a <b>north pole</b> and a <b>south pole</b>. The force is strongest at the poles.</li>"
             "<li><b>Like poles repel. Unlike poles attract.</b> A freely hanging magnet points north-south.</li>"
             "<li>Make a magnet by <b>stroking</b> a steel object in one direction with one pole, or by the <b>electrical method</b> (a coil of wire round an iron nail, connected to a battery).</li></ul>")
    ex = [("Two magnets push apart. What can you say about the facing poles?", ["Push apart means repel", "Like poles repel"], "They are the same pole (N–N or S–S)."),
          ("How can you make an electromagnet pick up more paper clips?", ["Add more coils of wire", "Or use more batteries"], "Make more coils or use more batteries.")]
    mist = ["Thinking all metals are magnetic. Aluminium, copper, gold and silver are not.",
            "Thinking a steel object that attracts a magnet must be a magnet. Only repulsion proves it is a magnet.",
            "Stroking back and forth when making a magnet. Stroke in one direction with one pole.",
            "Judging a magnet's strength by its size. Test it with paper clips."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Magnets and magnetic materials", B1 + [(MM.g_is, 4), (MM.g_pick, 4), (MM.g_table, 2), (MM.g_sort, 2)]),
        ("Poles: attract or repel", AR.B1 + [(AR.g_pic, 4), (AR.g_txt, 4), (AR.g_three, 2), (AR.g_train, 3), (g_through, 2)]),
        ("Making magnets", B2 + [(g_coil, 4), (MM.g_pick, 3), (AR.g_txt, 2), (g_through, 3)]),
        ("Uses of magnets", B3 + MM.B1 + [(AR.g_use, 5), (MM.g_sort, 3), (AR.g_strength, 2)]),
        ("PSLE-style investigations", B5 + AR.B5 + MM.B5 + [(AR.g_strength, 4), (g_coil, 4)]),
    ])
    make_sg(3, "magnets", 6, "Interactions", "Interaction of forces (Magnets)",
            "Recognise that magnets attract magnetic materials and that like poles repel and unlike poles attract; a freely suspended magnet comes to rest pointing north-south. "
            "Make a magnet by the stroke method and the electrical method, and compare the strength of magnets. Recognise uses of magnets in everyday life "
            "(summary of the MOE Primary Science Syllabus).",
            "Magnets",
            "Primary 3 Science: Magnets Worksheets (with Answers)",
            "Magnets",
            "Free Primary 3 science worksheets for Singapore pupils on magnets: magnetic materials, poles, attract and repel, making magnets and electromagnets, and uses of magnets. 100 questions with answers.",
            "Like poles repel; unlike poles attract.",
            "Magnets attract iron, steel, nickel and cobalt.",
            body(),
            [("Which materials does a magnet attract?", "Magnetic materials: iron, steel, nickel and cobalt. Aluminium, copper, plastic, wood and glass are not attracted."),
             ("How do I make a magnet?", "Stroke a steel object many times in one direction with one pole of a magnet, or wind a coil of wire around an iron nail and connect it to a battery."),
             ("How can I tell if an object is a magnet?", "Bring it near each pole of a known magnet. If it repels one of the poles, it is a magnet.")],
            sets)


if __name__ == "__main__":
    main()
