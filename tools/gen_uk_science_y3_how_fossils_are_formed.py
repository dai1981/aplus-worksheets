# -*- coding: utf-8 -*-
"""
UK Year 3 science: How Fossils Are Formed (Rocks)
  python tools/gen_uk_science_y3_how_fossils_are_formed.py
How fossils form when things that have lived are trapped within rock, the order of the steps, body and trace
fossils, what is and is not a fossil, reading undisturbed rock layers (oldest at the bottom), what fossils tell us,
and Mary Anning, the fossil hunter of Lyme Regis.
Reuses the step, layer, type and clue questions of the Year 6 fossils unit (new seed) and adds Year 3 questions.
Wrong answers come from real mistakes: "fossils are bones that are still bone", "fossils form in a few years",
"every animal becomes a fossil", "the top layer of rock is the oldest".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, People, once
import gen_uk_science_y6_fossils as F6

F6.U = Unit(61308)
F6.R = F6.U.R
F6.P = People(F6.R)
uk_sci.USED.clear()
U, R, P = F6.U, F6.R, F6.P

YES = ["an ammonite shell turned to stone", "a dinosaur footprint in rock", "a fish skeleton pressed into stone", "a fern leaf print in shale", "a shark tooth found in chalk",
       "a trilobite in a slab of rock", "an insect trapped in amber", "a sea urchin made of flint", "a dinosaur bone turned to stone", "a shell print in limestone"]
NO = ["a pebble from the beach", "a crystal of quartz", "a chicken bone from last night's dinner", "a seashell washed up today", "a plastic toy dinosaur",
      "a lump of coal-black obsidian", "a conker from last autumn", "a feather found in the garden", "a piece of brick", "a leaf that fell yesterday"]


def g_isfos():
    k = R.random() < 0.5
    if k:
        a = R.choice(YES)
        w = R.sample(NO, 3)
        if not once(("fy", a)):
            return None
        o = sorted([a] + w)
        return item("Which of these is a fossil: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "A fossil is the remains or trace of a living thing from long ago, preserved in rock.")
    a = R.choice(NO)
    w = R.sample(YES, 3)
    if not once(("fn", a)):
        return None
    o = sorted([a] + w)
    return item("Which of these is NOT a fossil: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "%s is not the preserved remains of a living thing from millions of years ago." % (a[0].upper() + a[1:]))


B1 = bank([
    ("What is a fossil?", "the remains or trace of a plant or animal from long ago, preserved in rock", ["any shiny stone", "a living animal", "a kind of crystal"], "Usually millions of years old."),
    ("In which kind of rock are most fossils found?", "sedimentary rock", ["igneous rock", "metamorphic rock", "glass"], "Layers of mud and sand bury the remains."),
    ("Why must a dead animal be covered quickly to become a fossil?", "so it is not eaten or rotted away first", ["so it stays warm", "so it can breathe", "so it stays soft"], "Mud or sand protects it."),
    ("Which parts of an animal usually become fossils?", "hard parts such as bones, teeth and shells", ["only the eyes", "only the skin and fur", "only the stomach"], "Soft parts rot away."),
    ("How long does it take for a fossil to form?", "millions of years", ["a few days", "one year", "about a week"], "Rock forms very slowly."),
    ("Where are fossils often found in the UK?", "on beaches and cliffs, such as the Jurassic Coast", ["inside houses", "in clouds", "in rivers of lava"], "Waves wear away the rock."),
    ("Does every animal that dies become a fossil?", "No. Most rot away or are eaten; fossils are rare.", ["Yes, always.", "Only cats.", "Only animals that die in winter."], "It needs just the right conditions."),
    ("What replaces the bone in a fossil, slowly over time?", "minerals, which turn it to stone", ["water", "air", "plastic"], "The fossil is rock in the shape of the bone."),
])
B4 = bank([
    ("Who was Mary Anning?", "a fossil hunter from Lyme Regis who found many important fossils", ["a famous astronaut", "a queen of England", "an inventor of the telephone"], "She lived about 200 years ago."),
    ("What did Mary Anning and her brother find when she was about 12?", "the first complete skeleton of an ichthyosaur", ["a living dinosaur", "a gold crown", "a new planet"], "A sea reptile like a dolphin."),
    ("Why did Mary Anning search for fossils after storms?", "Storms and waves broke off cliff rock and uncovered new fossils.", ["Fossils fall from the sky in storms.", "Storms make fossils grow.", "The beach was empty only then."], "Fresh rock is exposed."),
    ("Where did Mary Anning live?", "Lyme Regis in Dorset", ["London", "Edinburgh", "Cardiff"], "On the Jurassic Coast."),
    ("Why was Mary Anning's work important?", "It helped scientists understand that animals lived and died out long ago.", ["She invented fossils.", "She proved fossils were fake.", "She discovered dinosaurs were still alive."], "Evidence of extinction."),
    ("Why did Mary Anning sell some fossils?", "Her family was poor and needed the money.", ["Fossils were worthless.", "She did not like them.", "It was against the law to keep them."], "She sold them to collectors."),
    ("What is a palaeontologist?", "a scientist who studies fossils", ["a doctor for teeth", "a weather forecaster", "a space scientist"], "Mary Anning was an early one."),
    ("What did Mary Anning also find at Lyme Regis?", "a plesiosaur, a sea reptile with a very long neck", ["a woolly mammoth", "a living dodo", "a whale skeleton made of gold"], "Another important find."),
])
B5 = bank([
    ("Fossil seashells are found high in the hills. What does this tell us?", "The land was once under the sea.", ["Seabirds dropped them.", "Shells grow on hills.", "It tells us nothing."], "Fossils are clues."),
    ("Why are there so few fossils of jellyfish?", "Jellyfish have no hard parts, so they usually rot away.", ["Jellyfish never lived long ago.", "They are too big.", "They lived on land."], "Hard parts last."),
    ("Why should you not hammer cliffs to find fossils?", "It is dangerous and can cause rocks to fall.", ["Hammers make fossils vanish.", "Fossils are only in museums.", "Cliffs are made of glass."], "Look on the beach instead."),
    ("A footprint fossil is found. What can it tell scientists?", "the size of the animal and how it walked", ["the colour of its skin", "the sound it made", "its name"], "Trace fossils show behaviour."),
    ("How do fossils help us know about dinosaurs?", "Fossil bones and footprints show their size, shape and how they lived.", ["We have seen living dinosaurs.", "Dinosaurs wrote books.", "Fossils are photographs."], "Evidence from the past."),
])


def body():
    think = ("<p><b>A fossil forms when a living thing is trapped in rock.</b></p>"
             "<ul><li>A plant or animal dies and is quickly buried in mud or sand. Soft parts rot away.</li>"
             "<li>Layers build up and press down; minerals slowly replace the hard parts and turn them to stone.</li>"
             "<li>In undisturbed rock, the lowest layers are the oldest. Mary Anning found famous fossils at Lyme Regis.</li></ul>")
    ex = [("After burial in mud, what next?", ["Soft parts rot"], "the soft parts rot away"),
          ("Which layer has the oldest fossils?", ["Layers build up on top"], "the bottom layer")]
    mist = ["Thinking fossils form in a few years.", "Thinking every animal becomes a fossil.", "Thinking the top layer of rock is the oldest."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What is a fossil?", B1 + [(g_isfos, 8), (F6.g_step, 4)]),
        ("How fossils form", [(F6.g_step, 6), (F6.g_type, 9), (g_isfos, 5)]),
        ("Rock layers", [(F6.g_layer, 14), (F6.g_clue, 6)]),
        ("Mary Anning", B4 + [(F6.g_layer, 8), (g_isfos, 4)]),
        ("Fossil clues", B5 + [(F6.g_layer, 8), (g_isfos, 2), (F6.g_clue, 1)]),
    ])
    make_uk(3, "how-fossils-are-formed", 8, "Rocks",
            "Describe in simple terms how fossils are formed when things that have lived are trapped within rock.",
            "How Fossils Are Formed",
            "Year 3 Science: How Fossils Are Formed Worksheets (Rock Layers and Mary Anning)",
            "Fossils",
            "Free Year 3 science worksheets on fossils: how fossils form in rock, body and trace fossils, rock layers, what fossils tell us, and Mary Anning. 100 questions with answers.",
            "Trapped in rock for millions of years.",
            "Buried, pressed, turned to stone, then found.",
            body(),
            [("How is a fossil formed?", "A plant or animal dies and is quickly buried by mud or sand. The soft parts rot. Over millions of years the layers turn to rock and minerals replace the hard parts, making a stone copy."),
             ("Which rock layer is the oldest?", "In rock that has not been disturbed, the bottom layer is the oldest, because new layers form on top."),
             ("Who was Mary Anning?", "A fossil hunter who lived in Lyme Regis about 200 years ago. She found the first complete ichthyosaur skeleton and other important fossils.")],
            sets)


if __name__ == "__main__":
    main()
