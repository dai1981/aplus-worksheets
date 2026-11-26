# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Synthetic Materials (MS-PS1-3)
  python tools/gen_us_science_g7_synthetic_materials.py
Gather and make sense of information to describe that synthetic materials come from natural resources and
impact society: plastics, nylon and polyester from petroleum; synthetic rubber; medicines (aspirin from
willow bark chemistry); fertilizers from nitrogen in the air; Kevlar; glass from sand. Chemical processes
change natural resources into new substances. Benefits and problems (pollution, waste, microplastics).
Wrong answers come from real mistakes: "synthetic means it comes from nowhere", "synthetic materials are
always bad", "cotton is synthetic".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(70103)
R = U.R
P = People(R)

SYN = [("plastic bottles", "petroleum (oil)"), ("nylon rope", "petroleum (oil)"), ("polyester shirts", "petroleum (oil)"), ("synthetic rubber tires", "petroleum (oil)"),
       ("aspirin", "chemicals first found in willow bark"), ("fertilizer", "nitrogen from the air and natural gas"), ("Kevlar vests", "petroleum (oil)"),
       ("nonstick pan coating", "minerals and chemicals from natural resources"), ("polystyrene foam cups", "petroleum (oil)"), ("acrylic paint", "petroleum (oil)")]
NAT = ["cotton", "wool", "silk", "wood", "leather", "natural rubber from trees", "granite", "bamboo", "beeswax", "linen from flax plants"]


def g_kind():
    who = P.next()[0]
    if R.random() < 0.5:
        x = R.choice(SYN)[0]
        return item("%s sorts materials. Which one is synthetic (made by people through chemical processes)?" % who, x, R.sample(NAT, 3),
                    "Synthetic materials are made by changing natural resources with chemical reactions.")
    return item("%s sorts materials. Which one is natural (used mostly as it is found)?" % who, R.choice(NAT), R.sample([s for s, _ in SYN], 3),
                "Natural materials come from plants, animals or rocks without a chemical reaction making a new substance.")


def g_source():
    x, src = R.choice(SYN)
    who = P.next()[0]
    others = sorted({s for _, s in SYN if s != src}) + ["nothing; synthetic materials do not come from natural resources", "seawater only"]
    return item("%s reads about how %s are made. Which natural resource do they mainly come from?" % (who, x), src, R.sample(others, 3),
                "Every synthetic material is made from natural resources that are changed by chemical processes.")


IMPACT = [("plastic", "cheap, light and waterproof packaging that keeps food fresh", "plastic waste in oceans that harms sea animals"),
          ("synthetic fertilizer", "much larger crops that feed more people", "runoff that pollutes rivers and lakes"),
          ("nylon and polyester", "strong, quick-drying clothes and ropes", "tiny plastic fibers that wash into water"),
          ("synthetic medicines", "treatments that save many lives", "pollution from factories if wastes are not handled well"),
          ("Kevlar", "strong, light protective vests and helmets", "it is hard to recycle"),
          ("foam cups and packaging", "light, insulating containers", "trash that lasts hundreds of years in landfills")]


def g_impact():
    m, good, bad = R.choice(IMPACT)
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s is writing about %s. Which is a benefit to society?" % (who, m), good, [i[2] for i in IMPACT if i[0] != m][:3],
                    "Synthetic materials can help people in many ways.")
    return item("%s is writing about %s. Which is a problem it can cause?" % (who, m), bad, [i[1] for i in IMPACT if i[0] != m][:3],
                "Synthetic materials can also harm the environment.")


def g_steps():
    who = P.next()[0]
    chains = [("plastic bottle", ["Oil is pumped from the ground.", "Oil is separated and heated to make small molecules.", "Small molecules are joined into long chains (polymers).", "The plastic is melted and shaped into bottles."]),
              ("glass jar", ["Sand is dug from the ground.", "Sand is mixed with soda ash and limestone.", "The mixture is heated until it melts.", "The melted glass is shaped and cooled."]),
              ("nylon jacket", ["Oil is pumped from the ground.", "Chemicals are made from the oil.", "The chemicals react to form nylon.", "Nylon is spun into threads and woven."])]
    name, steps = R.choice(chains)
    i = R.randrange(3)
    return item("%s traces how a %s is made. What comes right after “%s”?" % (who, name, steps[i]), steps[i + 1],
                [s for s in steps if s not in (steps[i], steps[i + 1])][:2] + ["The finished product grows on a tree."], "The steps are: " + " → ".join(steps))


B1 = bank([
    ("What is a synthetic material?", "a material made by people using chemical processes to change natural resources", ["a material that appears from nothing", "a material found as it is in nature", "only metal"],
     "Plastics and nylon are synthetic."),
    ("Do synthetic materials come from natural resources?", "Yes. All of them start from natural resources like oil, minerals or air.", ["No, they come from nowhere.", "Only some come from plants.", "No, they are made of light."],
     "Chemical reactions change the resources into new substances."),
    ("Which natural resource is used to make most plastics?", "petroleum (oil)", ["cotton", "wood", "iron"], "Oil contains carbon-based molecules that are turned into plastics."),
    ("Why are synthetic materials important to society?", "They provide useful products like medicine, clothing and packaging.", ["They have no uses.", "They are only for decoration.", "They make natural materials disappear."],
     "Many modern products depend on them."),
    ("Which is a natural fiber?", "wool", ["polyester", "nylon", "acrylic"], "Wool comes from sheep."),
    ("Why can plastic waste be a problem?", "Many plastics do not break down for hundreds of years.", ["Plastic dissolves in rain.", "Plastic turns into oil.", "Plastic is good food for fish."],
     "Plastic pollution harms wildlife."),
    ("What is a polymer?", "a very long molecule made of many repeating small units", ["a single atom", "a kind of rock", "a natural fiber only"], "Plastics, nylon and DNA are polymers."),
    ("Why was synthetic rubber developed?", "Natural rubber from trees was not enough to meet the demand.", ["Natural rubber does not exist.", "Synthetic rubber grows on trees.", "To make tires heavier."],
     "Society's needs drive new materials."),
])
B5 = bank([
    ("Ava compares a cotton shirt and a polyester shirt. Which statement is true?", "Cotton comes from a plant; polyester is made from oil.", ["Both come from sheep.", "Polyester comes from cotton plants.", "Cotton is made in a lab from oil."],
     "Natural and synthetic fibers have different sources."),
    ("Leo reads that a new bioplastic is made from corn. What natural resource is it made from?", "corn plants", ["petroleum only", "sand", "iron ore"], "Synthetic materials can come from many natural resources."),
    ("Mia wants to reduce plastic waste at school. Which plan helps most?", "use reusable bottles and recycle plastics", ["buy more single-use bottles", "burn plastic outdoors", "throw plastics in rivers"],
     "Reduce, reuse and recycle."),
    ("A company makes a stronger, lighter plastic for car parts. How could this help society?", "Lighter cars use less fuel.", ["Cars become heavier.", "It uses no resources.", "It cannot be used."],
     "New materials can save energy."),
    ("Why do scientists study how synthetic materials affect the environment?", "to reduce harmful effects while keeping the benefits", ["to stop making all materials", "because they only care about cost", "to make materials last forever in oceans"],
     "Balancing benefits and costs."),
])


def body():
    think = ("<p><b>Synthetic materials</b> are made by people. Chemists use <b>chemical reactions</b> to change <b>natural resources</b> into new substances with useful properties.</p>"
             "<ul><li>Plastics, nylon, polyester and synthetic rubber come from <b>petroleum (oil)</b>.</li>"
             "<li>Fertilizer is made from nitrogen in the air and natural gas.</li>"
             "<li>Some medicines, like aspirin, are based on chemicals first found in plants.</li></ul>"
             "<p>Synthetic materials help society (cheap packaging, strong fabrics, medicines) but can also cause problems (plastic pollution, factory waste).</p>")
    ex = [("Is nylon natural or synthetic?", ["It is made from oil by chemical reactions."], "synthetic"),
          ("What natural resource is used to make plastic bottles?", ["Plastic polymers are made from oil."], "petroleum (oil)")]
    mist = ["Thinking synthetic materials do not come from natural resources.",
            "Thinking synthetic materials are always harmful; many help people.",
            "Calling cotton or wool synthetic."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Natural and synthetic", B1 + [(g_kind, 12)]),
        ("Where synthetic materials come from", [(g_source, 14), (g_kind, 6)]),
        ("How materials are made", [(g_steps, 12), (g_source, 8)]),
        ("Impacts on society", [(g_impact, 14), (g_kind, 6)]),
        ("Making sense of information", B5 + [g_impact, g_steps, g_source, g_kind]),
    ])
    make("grade-7", "synthetic-materials", 3, "MS-PS1-3",
         "Gather and make sense of information to describe that synthetic materials come from natural resources and impact society.",
         "Synthetic Materials",
         "Grade 7 Synthetic Materials Worksheets: Plastics, Nylon and Natural Resources",
         "Synthetic Materials",
         "Free middle school science worksheets on synthetic materials (NGSS MS-PS1-3): natural vs. synthetic materials, plastics and fibers made from oil, how materials are made, and their impacts on society. 100 practice questions with answers.",
         "Synthetic materials are made from natural resources.",
         "Chemical reactions turn oil, minerals and air into plastics, fabrics, medicines and fertilizers that affect our lives and the environment.",
         body(),
         [("What is a synthetic material?", "A material made by people using chemical reactions to change natural resources, like plastic made from oil."),
          ("Do synthetic materials come from nature?", "Yes. They all start as natural resources such as petroleum, minerals, plants or air."),
          ("How do synthetic materials affect society?", "They give us useful products like medicines and strong fabrics, but they can also cause pollution and waste.")],
         sets)


if __name__ == "__main__":
    main()
