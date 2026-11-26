# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Genes and Mutations (MS-LS3-1)
  python tools/gen_us_science_g8_genes_and_mutations.py
Develop and use a model to describe why structural changes to genes (mutations) located on chromosomes may affect
proteins and may result in harmful, beneficial, or neutral effects to the structure and function of the organism.
DNA → gene → protein → trait; substitution, insertion and deletion; examples (sickle cell, lactase persistence,
antibiotic resistance in bacteria, a silent change).
Wrong answers come from real mistakes: "all mutations are harmful", "a mutation changes every gene",
"proteins make DNA", "a mutation in a skin cell is passed to children".
"""
from sci_common import Unit, item, bank, lesson, make, People

U = Unit(80112)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def mono(s):
    return "<span style='font-family:monospace;letter-spacing:2px'>%s</span>" % s


def g_type():
    who = P.next()[0]
    n = R.choice([9, 10, 11, 12])
    seq = "".join(R.choice("ATGC") for _ in range(n))
    k = R.choice(["substitution", "insertion", "deletion"])
    i = R.randint(2, n - 3)
    if k == "substitution":
        new = seq[:i] + R.choice([b for b in "ATGC" if b != seq[i]]) + seq[i + 1:]
    elif k == "insertion":
        new = seq[:i] + R.choice("ATGC") + seq[i:]
    else:
        new = seq[:i] + seq[i + 1:]
    if new == seq or not once(("t", seq)):
        return None
    return item("%s compares a DNA sequence before and after a mutation.<br>Before: %s<br>After: %s<br>What kind of mutation is it?" % (who, mono(seq), mono(new)), k,
                [x for x in ["substitution", "insertion", "deletion"] if x != k] + ["no mutation"],
                {"substitution": "One base was swapped for another; the length stays the same.", "insertion": "An extra base was added, so the sequence is longer.",
                 "deletion": "A base was removed, so the sequence is shorter."}[k])


EFF = [("A mutation lets some bacteria survive an antibiotic.", "beneficial", "It helps the bacteria survive in that environment."),
       ("A mutation causes sickle-shaped red blood cells that carry less oxygen.", "harmful", "Less oxygen reaches the body."),
       ("A mutation lets some adults keep digesting milk sugar (lactose).", "beneficial", "It gives people another food source."),
       ("A mutation changes one base, but the protein made is exactly the same.", "neutral", "The protein and trait do not change."),
       ("A mutation stops a plant from making chlorophyll in its leaves.", "harmful", "The plant cannot make food by photosynthesis."),
       ("A mutation gives a moth darker wings that match sooty tree bark.", "beneficial", "Predators have a harder time seeing it on dark bark."),
       ("A mutation makes a cat's fur a slightly different shade with no effect on survival.", "neutral", "It does not help or hurt the cat."),
       ("A mutation causes a protein that helps blood clot to stop working.", "harmful", "Cuts bleed much longer."),
       ("A mutation lets an insect break down a pesticide.", "beneficial", "It survives where the pesticide is sprayed."),
       ("A mutation happens in a part of DNA that is never used to make a protein.", "neutral", "No protein changes, so the trait does not change."),
       ("A mutation makes an arctic hare's fur stay brown all winter in the snow.", "harmful", "Predators can see it easily in the snow."),
       ("A mutation gives a fish a slightly different fin color that predators and mates ignore.", "neutral", "It has no effect on survival or reproduction.")]


def g_eff():
    s, a, e = R.choice(EFF)
    who = P.next()[0]
    t = R.random() < 0.5
    if not once(("e", s, t)):
        return None
    if t:
        w = [x[2] for x in EFF if x[1] != a]
        return item("%s reads: “%s” This mutation is %s. Why?" % (who, s, a), e, R.sample(w, 3), "Effects depend on how the protein changes and on the environment.")
    return item("%s reads: “%s” Is this mutation harmful, beneficial or neutral?" % (who, s), a, [x for x in ["harmful", "beneficial", "neutral"] if x != a] + ["impossible"], e)


STEPS = ["DNA", "gene", "protein", "trait"]


def g_chain():
    who = P.next()[0]
    ex = R.choice([("eye color", "a pigment protein in the iris"), ("hair texture", "keratin proteins in hair"), ("blood type", "proteins on red blood cells"),
                   ("flower color", "enzymes that make pigments"), ("ability to digest lactose", "the enzyme lactase"), ("fur color in mice", "a pigment-making protein")])
    k = R.choice(["order", "protein", "how"])
    if not once(("c", ex[0], k)):
        return None
    if k == "order":
        return item("%s is modeling how genes affect %s. Which order is correct?" % (who, ex[0]), "gene → protein → trait",
                    ["trait → protein → gene", "protein → gene → trait", "gene → trait → protein"], "A gene is the instructions for a protein, and proteins build traits.")
    if k == "protein":
        return item("%s learns that %s depends on %s. What do genes provide?" % (who, ex[0], ex[1]), "the instructions to make the protein",
                    ["the protein itself", "the food for the cell", "energy for the trait"], "Genes are segments of DNA that code for proteins.")
    return item("A mutation changes the gene behind %s. According to %s's model, how could this change the trait?" % (ex[0], who), "The gene could make a different protein, which changes the trait.",
                ["The trait changes, and then the gene changes.", "Mutations never affect proteins.", "Every gene in the body changes."], "Changed gene → possibly changed protein → possibly changed trait.")


B1 = bank([
    ("What is a gene?", "a section of DNA that holds instructions for making a protein", ["a type of protein", "a whole chromosome", "a cell"], "Genes are on chromosomes."),
    ("Where are genes found?", "on chromosomes inside the nucleus of cells", ["in the cell wall only", "in the blood only", "outside the cell"], "Chromosomes are made of DNA."),
    ("What is a mutation?", "a change in the DNA sequence of a gene", ["a change in the weather", "a new organism", "a protein that is eaten"], "It changes the instructions."),
    ("Are all mutations harmful?", "No. They can be harmful, beneficial or neutral.", ["Yes, always.", "No, they are always helpful.", "They never have effects."], "It depends on the change and the environment."),
    ("Why can a change in a gene change a trait?", "The gene may make a different protein, and proteins determine traits.", ["Traits make genes.", "Genes are made of traits.", "Proteins are not related to traits."], "Gene → protein → trait."),
    ("Which mutation can be passed to offspring?", "a mutation in a sex cell (egg or sperm)", ["a mutation in a skin cell from sunburn", "a mutation in a muscle cell", "a mutation in a hair cell"], "Only sex cells pass DNA to offspring."),
    ("What can cause mutations?", "copying errors and things like UV light or certain chemicals", ["only eating sugar", "wearing blue clothes", "drinking water"], "Mutations can be random or caused by the environment."),
    ("How many bases are in DNA's code?", "four: A, T, G and C", ["two: 0 and 1", "26 letters", "ten"], "Adenine, thymine, guanine, cytosine."),
])
B4 = bank([
    ("A DNA sequence ATTGCA becomes ATTGGCA. How did the length change?", "It got 1 base longer, so it is an insertion.", ["It got shorter.", "It stayed the same length.", "It doubled."], "An extra G was added."),
    ("A DNA sequence CGTACT becomes CGACT. What happened?", "One base was deleted.", ["One base was added.", "One base was swapped.", "Nothing changed."], "The T was removed."),
    ("Which mutation keeps the DNA sequence the same length?", "a substitution", ["an insertion", "a deletion", "a duplication of a whole gene"], "One base swaps for another."),
    ("What is a model of a chromosome?", "a long strand of DNA wound up, with many genes along it", ["a single protein", "a cell membrane", "a single base"], "Chromosomes carry many genes."),
    ("Why do scientists say a mutation 'may' change a protein?", "Some base changes still code for the same protein.", ["Mutations always change proteins.", "Proteins have no code.", "Mutations only change chromosomes."], "Some changes are silent."),
    ("A mutation makes a protein fold into the wrong shape. Why does this matter?", "A protein's shape lets it do its job, so a wrong shape can stop it from working.", ["Shape does not matter.", "The protein becomes a gene.", "It becomes stronger always."],
     "Structure affects function."),
    ("How do mutations add variation to a population?", "They create new versions of genes that can be passed on.", ["They make everyone identical.", "They remove all genes.", "They only change the weather."], "Mutations are the source of new alleles."),
    ("Which organism could pass a new mutation to its offspring most quickly?", "bacteria, which reproduce every 20 minutes or so", ["an elephant", "a whale", "an oak tree"], "Fast reproduction spreads mutations fast."),
    ("UV light damages DNA in skin cells. Why is sunscreen helpful?", "It reduces UV that can cause mutations.", ["It adds new genes.", "It makes proteins.", "It changes eye color."], "Protecting DNA."),
    ("What is the job of most proteins made from genes?", "to build body parts and carry out cell functions", ["to store all DNA", "to make chromosomes", "to block sunlight"], "Proteins do the work in cells."),
])
B5 = bank([
    ("Ava says the same mutation could be helpful in one place and harmful in another. Which example supports her?", "Dark fur helps a mouse hide on dark rocks but makes it easy to see on light sand.", ["All white rabbits live in snow.", "Mutations never depend on the environment.", "Every mouse has the same fur."],
     "Effects depend on the environment."),
    ("Leo models a gene as a recipe and a protein as the dish. What does a mutation represent?", "a change in the recipe that may change the dish", ["a new kitchen", "eating the dish", "the cook's name"], "A good analogy."),
    ("Mia finds a mutation that does not change the protein. What effect will it most likely have?", "neutral, no change in the trait", ["very harmful", "very beneficial", "it changes every trait"], "Same protein, same trait."),
    ("Why might a deletion often cause a bigger change than a substitution?", "It can shift how the rest of the gene is read, changing many parts of the protein.", ["Deletions add new genes.", "Substitutions remove the whole gene.", "They always cause the same change."],
     "The reading frame shifts."),
    ("Bacteria with a resistance mutation survive an antibiotic and multiply. What happens to the population?", "More bacteria in the population have the resistance mutation.", ["All bacteria die.", "The mutation disappears.", "Nothing changes."],
     "Beneficial mutations can spread."),
])


def body():
    think = ("<p><b>Chromosomes</b> are made of <b>DNA</b>. A <b>gene</b> is a section of DNA with instructions for making a <b>protein</b>, and proteins shape <b>traits</b>.</p>"
             "<p><b>gene → protein → trait</b></p>"
             "<p>A <b>mutation</b> is a change in the DNA sequence: a <b>substitution</b> (one base swapped), an <b>insertion</b> (a base added) or a <b>deletion</b> (a base removed). "
             "A mutation can change the protein and the trait. The effect can be <b>harmful</b>, <b>beneficial</b> or <b>neutral</b>, often depending on the environment.</p>")
    ex = [("ATGCCA becomes ATGACA. Type?", ["Same length, one base changed."], "substitution"),
          ("A mutation lets insects survive a pesticide. Effect?", ["Helps survival."], "beneficial")]
    mist = ["Thinking all mutations are harmful.",
            "Thinking a mutation in a body cell, like a skin cell, is passed to children.",
            "Mixing up the order: genes code for proteins, not the other way around."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Genes and proteins", B1 + [(g_chain, 12)]),
        ("Types of mutations", [(g_type, 14), (g_chain, 6)]),
        ("Effects of mutations", [(g_eff, 12), (g_type, 8)]),
        ("Modeling mutations", B4 + [(g_type, 10)]),
        ("Explaining with evidence", B5 + [(g_eff, 7), (g_type, 8)]),
    ])
    make("grade-8", "genes-and-mutations", 12, "MS-LS3-1",
         "Develop and use a model to describe why structural changes to genes (mutations) located on chromosomes may affect proteins and may result in harmful, beneficial, or neutral effects to the structure and function of the organism.",
         "Genes and Mutations",
         "Grade 8 Genes and Mutations Worksheets: DNA, Proteins, Traits and Mutation Effects",
         "Genes and Mutations",
         "Free middle school science worksheets on genes and mutations (NGSS MS-LS3-1): how genes code for proteins and traits, substitutions, insertions and deletions, and harmful, beneficial and neutral mutations. 100 practice questions with answers.",
         "Gene → protein → trait.",
         "A mutation changes a gene's instructions. It may change the protein and the trait, with harmful, beneficial or neutral effects.",
         body(),
         [("What is the relationship between genes and proteins?", "A gene is a section of DNA that carries the instructions for making a protein. Proteins help determine an organism's traits."),
          ("Are mutations always bad?", "No. Mutations can be harmful, beneficial or neutral. The effect often depends on the organism's environment."),
          ("What are the main types of gene mutations?", "Substitution (one base is replaced), insertion (a base is added) and deletion (a base is removed).")],
         sets)


if __name__ == "__main__":
    main()
