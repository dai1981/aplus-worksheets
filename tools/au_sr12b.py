# -*- coding: utf-8 -*-
"""Year 12 Biology (Australian Curriculum: Senior Secondary Biology, Units 3 and 4) for au_sr.build."""
from au_sr import SR

BIO = "Biology"
GI = "genetic-information-and-variation"
GP = "genetics-populations-and-evolution"
GE = "gene-expression-and-biotechnology"
RH = "response-and-homeostasis"

DNA = [
    ("What are the three parts of a DNA nucleotide?", "a phosphate group, deoxyribose sugar and a nitrogenous base", ["a phosphate, ribose and uracil", "an amino acid, a sugar and a base", "a fatty acid, glycerol and a phosphate"], "RNA nucleotides have ribose instead."),
    ("Which bases pair in DNA?", "adenine with thymine, and cytosine with guanine", ["adenine with cytosine, and guanine with thymine", "adenine with uracil, and cytosine with guanine", "every base can pair with any other"], "A–T has two hydrogen bonds, C–G three."),
    ("What does semi-conservative replication mean?", "each new DNA molecule has one original strand and one new strand", ["both strands of the new molecule are new", "the original molecule is destroyed", "only one strand is copied"], "Shown by the Meselson–Stahl experiment."),
    ("What is a gene?", "a section of DNA that codes for a protein or functional RNA", ["a whole chromosome", "a single base", "a protein that copies DNA"], "Humans have about 20 000 protein-coding genes."),
    ("What is the genetic code?", "the sequence of base triplets (codons) that specifies amino acids", ["the order of chromosomes in a cell", "the number of genes in an organism", "the shape of a protein"], "It is universal and degenerate."),
    ("Why is the genetic code called degenerate?", "most amino acids are coded for by more than one codon", ["it changes over time", "it has errors", "each codon codes for several amino acids"], "There are 64 codons for 20 amino acids."),
    ("What happens during transcription?", "an mRNA copy of a gene is made from the DNA template strand in the nucleus", ["amino acids are joined at the ribosome", "DNA is copied before cell division", "proteins fold into shape"], "RNA polymerase does this."),
    ("What happens during translation?", "ribosomes read mRNA codons and tRNA brings the matching amino acids", ["DNA is copied into mRNA", "introns are added", "chromosomes are separated"], "Peptide bonds join the amino acids."),
    ("What are introns?", "non-coding sections of a gene that are removed from pre-mRNA", ["the coding sections that stay in mRNA", "start codons", "parts of ribosomes"], "The exons are joined in splicing."),
    ("What is the start codon in mRNA?", "AUG (methionine)", ["UAA", "UGA", "AAA"], "UAA, UAG and UGA are stop codons."),
    ("What is the role of tRNA?", "it carries a specific amino acid and has an anticodon that pairs with the mRNA codon", ["it carries the genetic code out of the nucleus", "it forms the ribosome", "it unzips DNA"], "The anticodon is complementary to the codon."),
    ("What is a promoter?", "a DNA sequence near the start of a gene where RNA polymerase binds", ["a stop codon", "an amino acid", "a type of mutation"], "Transcription factors help RNA polymerase bind."),
    ("How can two cells with the same DNA, such as a nerve cell and a muscle cell, be so different?", "different genes are switched on (expressed) in each cell", ["they have different genes", "one cell has lost its DNA", "they come from different organisms"], "Gene regulation controls differentiation."),
    ("What is the structure of a eukaryotic chromosome?", "a long DNA molecule wound around histone proteins", ["a circular DNA molecule with no proteins", "a chain of amino acids", "a single gene"], "Prokaryotes have circular DNA and often plasmids."),
]
INH = [
    ("What is an allele?", "a different form of the same gene", ["a section of a chromosome with many genes", "a type of cell division", "a protein"], "For example, alleles for blood group A, B and O."),
    ("What does homozygous mean?", "having two identical alleles of a gene", ["having two different alleles", "having one allele", "having no alleles"], "BB and bb are homozygous."),
    ("What is the phenotype of an organism?", "its observable characteristics, produced by genotype and environment", ["its set of alleles", "the number of its chromosomes", "the DNA sequence of one gene"], "Genotype + environment → phenotype."),
    ("What is the expected ratio of phenotypes from a cross between two heterozygotes (Aa × Aa) for a dominant trait?", "3 dominant : 1 recessive", ["1 : 1", "1 : 2 : 1 phenotypes", "all dominant"], "The genotype ratio is 1 AA : 2 Aa : 1 aa."),
    ("What is a test cross?", "crossing an organism of unknown genotype with a homozygous recessive", ["crossing two heterozygotes", "crossing two homozygous dominants", "crossing an organism with itself"], "Any recessive offspring show the unknown parent is heterozygous."),
    ("Why are sex-linked recessive conditions such as red–green colour blindness more common in males?", "males have one X chromosome, so a single recessive allele is expressed", ["males have two X chromosomes", "the allele is on the Y chromosome", "females cannot inherit it"], "Females need two copies to show the trait."),
    ("A colour-blind man and a woman who is not a carrier have a son. What is the chance the son is colour-blind?", "0, because the son gets his X chromosome from his mother", ["100%", "50%", "25%"], "Fathers pass their Y to sons."),
    ("In a pedigree, two unaffected parents have an affected child. What does this show?", "the trait is recessive and both parents are carriers", ["the trait is dominant", "the trait is sex-linked dominant", "the trait cannot be inherited"], "A dominant trait would show in a parent."),
    ("What is codominance?", "both alleles are fully expressed in the heterozygote, such as blood group AB", ["one allele hides the other", "the heterozygote shows a blend", "neither allele is expressed"], "Incomplete dominance gives a blend, such as pink flowers."),
    ("What is crossing over?", "exchange of sections between homologous chromosomes during prophase I of meiosis", ["copying of DNA", "separation of sister chromatids in mitosis", "fusion of gametes"], "It makes new combinations of alleles."),
    ("How does meiosis produce genetic variation?", "by crossing over and independent assortment of homologous chromosomes", ["by making identical cells", "by doubling the chromosome number", "by copying mutations exactly"], "Random fertilisation adds more variation."),
    ("How many chromosomes are in a human gamete?", "23", ["46", "92", "22"], "Gametes are haploid."),
    ("What is non-disjunction?", "chromosomes failing to separate in meiosis, giving gametes with an extra or missing chromosome", ["a type of point mutation", "crossing over", "a dominant allele"], "Trisomy 21 (Down syndrome) can result."),
    ("Which is a polygenic trait?", "human height", ["blood group ABO", "cystic fibrosis", "red–green colour blindness"], "Many genes plus environment give continuous variation."),
]
BIOT = [
    ("What is a point mutation?", "a change in a single base, by substitution, insertion or deletion", ["the loss of a whole chromosome", "a change in the number of chromosome sets", "a change in a protein only"], "Sickle-cell anaemia is caused by one base substitution."),
    ("Why does an insertion or deletion of one base usually have a big effect?", "it shifts the reading frame, changing every codon after it", ["it changes only one amino acid", "it never changes the protein", "it doubles the gene"], "This is a frameshift mutation."),
    ("What is a silent mutation?", "a base change that does not change the amino acid, because the code is degenerate", ["a mutation that stops all transcription", "a deletion of a gene", "a mutation that changes many amino acids"], "The protein is unchanged."),
    ("What is a mutagen?", "a factor that increases the rate of mutation, such as UV radiation or some chemicals", ["a protein that repairs DNA", "a type of chromosome", "a gene that controls growth"], "Australia has high UV levels and high skin cancer rates."),
    ("Why are mutations important for evolution?", "they are the original source of new alleles and genetic variation", ["they always harm organisms", "they stop natural selection", "they make every organism identical"], "Most are neutral; some are harmful, a few helpful."),
    ("What do restriction enzymes do?", "cut DNA at specific base sequences", ["join DNA fragments", "copy DNA", "translate mRNA"], "They often leave sticky ends."),
    ("What does DNA ligase do?", "joins DNA fragments by forming bonds between nucleotides", ["cuts DNA", "unzips DNA", "makes mRNA"], "It seals a gene into a plasmid."),
    ("What is the role of PCR?", "to make millions of copies of a DNA sequence", ["to cut DNA", "to separate DNA by size", "to translate DNA into protein"], "Each cycle doubles the DNA."),
    ("What are the three temperature steps in each PCR cycle?", "denaturing (about 95 °C), annealing primers (about 55 °C) and extension (about 72 °C)", ["freezing, thawing and boiling", "cutting, ligating and cloning", "37 °C only"], "A heat-stable polymerase (Taq) is used."),
    ("In gel electrophoresis, why do DNA fragments move towards the positive electrode?", "DNA is negatively charged because of its phosphate groups", ["DNA is positively charged", "the gel pushes them", "they are attracted by the dye"], "Smaller fragments move further."),
    ("What is a recombinant plasmid?", "a bacterial plasmid with a gene from another organism inserted into it", ["a plasmid with no genes", "a viral chromosome", "a plasmid made of protein"], "Used to make insulin in bacteria."),
    ("What is CRISPR-Cas9 used for?", "editing a specific DNA sequence by cutting it with a guide RNA", ["making copies of DNA", "separating DNA by size", "staining chromosomes"], "It can knock out or change genes."),
    ("What is a genetically modified organism (GMO)?", "an organism whose DNA has been changed using gene technology", ["an organism bred by selective breeding only", "an organism with a natural mutation", "a cloned organism with no changes"], "Bt cotton is widely grown in Australia."),
    ("Why is Bt cotton grown in Australia?", "it contains a bacterial gene that makes a protein toxic to caterpillar pests, reducing insecticide use", ["it grows without water", "it makes cotton blue", "it fixes nitrogen"], "Insecticide sprays fell by up to 85%."),
    ("How is DNA profiling used in forensic science?", "comparing the lengths of short tandem repeats from crime-scene DNA and suspects", ["reading a person's whole genome every time", "looking at fingerprints", "measuring blood groups only"], "STR patterns are almost unique to each person."),
    ("What is an ethical issue with genetic testing?", "privacy: insurers or employers might use the results", ["it uses no DNA", "it is always 100% accurate", "it changes a person's genes"], "Genetic counselling helps people decide."),
]
EVO = [
    ("What does natural selection need to act on?", "heritable variation in a population", ["identical individuals", "acquired characteristics", "changes that happen in one lifetime only"], "Variation comes from mutation and sexual reproduction."),
    ("Which statement about natural selection is correct?", "individuals with favourable alleles survive and reproduce more, so those alleles become more common", ["individuals change their genes to suit the environment", "animals evolve because they need to", "every individual has the same chance of survival"], "Populations evolve, not individuals."),
    ("What is a gene pool?", "all the alleles of all the genes in a population", ["all the genes in one cell", "a pond where genes are studied", "the genes of one species in a zoo"], "Evolution is a change in allele frequencies."),
    ("What is genetic drift?", "random changes in allele frequency, strongest in small populations", ["changes caused by natural selection", "movement of alleles between populations", "mutations caused by radiation"], "Alleles can be lost by chance."),
    ("What is the founder effect?", "a new population started by a few individuals has different allele frequencies from the original", ["the effect of the first species in an area", "the oldest individual controlling a group", "a mutation in a founder gene"], "Island populations often show it."),
    ("What is a genetic bottleneck?", "a sharp fall in population size that reduces genetic diversity", ["a mutation that blocks a gene", "a narrow river that separates populations", "a type of natural selection"], "Cheetahs and Tasmanian devils show low diversity."),
    ("What is gene flow?", "movement of alleles between populations by migration", ["the copying of genes", "random changes in small populations", "the loss of genes"], "It makes populations more similar."),
    ("What is allopatric speciation?", "new species form after populations are separated by a geographical barrier", ["new species form in the same place", "species merge", "a species dies out"], "Bass Strait separated Tasmanian populations."),
    ("Which is an example of reproductive isolation?", "two frog species breed at different times of the year", ["two frogs live in the same pond", "two frogs eat the same insects", "two frogs are the same colour"], "Temporal isolation stops interbreeding."),
    ("What is convergent evolution?", "unrelated species evolve similar features because they live in similar environments", ["related species become more different", "species interbreed", "species stay the same"], "Marsupial sugar gliders and placental colugos of South-East Asia both glide."),
    ("What is divergent evolution (adaptive radiation)?", "a common ancestor gives rise to many species adapted to different niches", ["unrelated species become alike", "a species stays unchanged", "species lose all variation"], "Australian marsupials radiated into many niches."),
    ("Which is evidence for evolution from comparative anatomy?", "homologous structures, such as the same bones in a human arm and a bat wing", ["analogous structures prove a close relationship", "all animals have the same number of legs", "fossils are always complete"], "Homologous = same ancestry, different function."),
    ("What does molecular evidence show about the relationships of species?", "species with more similar DNA or protein sequences share a more recent common ancestor", ["DNA cannot show relationships", "all species have identical DNA", "only body shape shows relationships"], "Molecular clocks estimate divergence times."),
    ("Why have many rabbits in Australia become resistant to myxomatosis?", "rabbits with resistance survived and passed on their alleles", ["the virus made the rabbits change", "rabbits learnt to avoid it", "the virus disappeared"], "The virus also evolved to be less lethal."),
    ("Why have cane toads at the invasion front in northern Australia evolved longer legs?", "faster-moving toads reach new areas first and breed there", ["toads stretch their legs", "long legs are caused by the climate", "all toads have the same legs"], "This is spatial sorting plus selection."),
    ("What is the Hardy–Weinberg principle used for?", "testing whether allele frequencies in a population are changing", ["counting chromosomes", "measuring biodiversity", "dating fossils"], "p² + 2pq + q² = 1 and p + q = 1."),
]
HOME = [
    ("What is homeostasis?", "keeping the internal environment within narrow limits", ["changing the internal environment to match the outside", "growing larger", "removing all waste"], "Body temperature, blood glucose and water balance are examples."),
    ("What is negative feedback?", "a response that reverses a change and returns a variable to its set point", ["a response that makes a change bigger", "no response to a change", "a nerve impulse only"], "Most homeostatic control is by negative feedback."),
    ("Which is an example of positive feedback?", "oxytocin increasing contractions during childbirth", ["sweating when hot", "insulin lowering blood glucose", "shivering when cold"], "Positive feedback amplifies a change."),
    ("What are the parts of a stimulus–response model?", "stimulus → receptor → control centre → effector → response", ["effector → receptor → stimulus", "hormone → nerve → muscle only", "response → stimulus → receptor"], "In negative feedback the response reduces the stimulus."),
    ("Which part of the brain controls body temperature?", "the hypothalamus", ["the cerebellum", "the medulla only", "the pituitary only"], "It receives information from thermoreceptors."),
    ("How does the body lose heat on a hot day?", "sweating and vasodilation of skin blood vessels", ["shivering", "vasoconstriction", "raising hairs"], "More blood flows near the skin surface."),
    ("How does the body reduce heat loss on a cold day?", "vasoconstriction of skin blood vessels and shivering", ["sweating more", "vasodilation", "drinking more water"], "Shivering makes heat by respiration."),
    ("How do red kangaroos cool down in the desert?", "they lick their forearms so evaporation cools the blood in surface vessels", ["they shiver", "they increase metabolic rate", "they bask in the sun"], "They also rest in shade during the day."),
    ("Why are lizards called ectotherms?", "they get most of their body heat from the environment and control temperature by behaviour", ["they make heat by respiration like mammals", "they have no body temperature", "they live only in cold places"], "Basking and shade-seeking are behaviours."),
    ("Which hormone lowers blood glucose?", "insulin", ["glucagon", "adrenaline", "ADH"], "It is made by beta cells in the pancreas."),
    ("Which hormone raises blood glucose?", "glucagon", ["insulin", "ADH", "oxytocin"], "It stimulates the liver to break down glycogen."),
    ("What is the role of ADH (antidiuretic hormone)?", "it makes the collecting ducts more permeable, so more water is reabsorbed", ["it makes the kidneys remove more water", "it lowers blood glucose", "it raises body temperature"], "Released when blood is too concentrated."),
    ("How does the spinifex hopping mouse survive with almost no drinking water?", "its kidneys make very concentrated urine", ["it stores water in its tail", "it drinks sea water", "it never loses water"], "Its loop of Henle is very long."),
    ("What is the difference between nervous and hormonal control?", "nerves are fast, short-lived and targeted; hormones are slower, longer-lasting and travel in the blood", ["hormones are faster", "nerves travel in the blood", "they are the same"], "Both coordinate responses."),
    ("What is a synapse?", "a small gap between neurons where neurotransmitters carry the signal", ["the cell body of a neuron", "a type of hormone", "a muscle fibre"], "Synapses make impulses travel in one direction."),
    ("What is type 1 diabetes?", "a condition in which the pancreas makes little or no insulin", ["a condition caused only by eating sugar", "too much insulin", "kidney failure"], "It is treated with insulin injections."),
    ("How do plants respond to light coming from one side?", "auxin moves to the shaded side, so cells there elongate and the shoot bends towards the light", ["the shoot grows away from light", "cells on the light side grow faster", "plants do not respond"], "This is positive phototropism."),
    ("What is the normal core body temperature of a human?", "about 37 °C", ["about 33 °C", "about 40 °C", "about 25 °C"], "Enzymes work best near this temperature."),
    ("Why can a core temperature above about 40 °C be dangerous?", "enzymes and other proteins start to denature, so body processes fail", ["blood freezes", "the heart stops making blood", "cells stop dividing for ever"], "This is heatstroke."),
    ("What is hypothermia?", "a core body temperature below about 35 °C", ["a high body temperature", "low blood glucose", "dehydration"], "Shivering stops in severe hypothermia."),
    ("What is an endotherm?", "an animal that keeps its body temperature constant mainly with heat from its own metabolism", ["an animal whose temperature matches its surroundings", "a cold-blooded reptile", "a plant"], "Mammals and birds are endotherms."),
    ("Why do small mammals lose heat faster than large mammals?", "they have a larger surface area to volume ratio", ["they have a smaller surface area to volume ratio", "they have no fur", "they have a higher body temperature"], "Small mammals need a high metabolic rate."),
    ("How does fur or feathers reduce heat loss?", "they trap a layer of still air, which is a poor conductor of heat", ["they absorb heat from the blood", "they make the animal sweat", "they reflect all heat inwards"], "Raised hairs trap a thicker layer."),
    ("What is torpor?", "a short period of lowered body temperature and metabolism to save energy", ["a fever", "an increase in metabolic rate", "a type of shivering"], "Many small marsupials and bats use torpor on cold nights."),
    ("How do thermoreceptors help control body temperature?", "they detect temperature changes in the skin and blood and send signals to the hypothalamus", ["they make heat", "they release insulin", "they control breathing only"], "They are the receptors in the feedback loop."),
    ("What is counter-current heat exchange in the legs of wading birds?", "warm arterial blood heats cooler venous blood returning to the body, so less heat is lost from the feet", ["blood flows faster in cold water", "feathers cover the feet", "the feet produce heat"], "Arteries and veins lie side by side."),
    ("Why do humans sweat more in dry heat than in humid heat to get the same cooling?", "sweat evaporates easily in dry air; in humid air evaporation is slow and less cooling happens", ["humid air is colder", "sweat cannot form in humid air", "dry air contains more water"], "Humid heat is more dangerous."),
    ("What happens to the heart rate during exercise, and why?", "it rises, to deliver more oxygen and glucose to muscles and remove CO₂", ["it falls, to save energy", "it stays exactly the same", "it stops briefly"], "The medulla detects rising CO₂."),
    ("Which receptors detect a rise in blood concentration (osmotic pressure)?", "osmoreceptors in the hypothalamus", ["thermoreceptors in the skin", "photoreceptors in the eye", "pain receptors"], "The pituitary then releases ADH."),
    ("Why is a fever helpful during an infection?", "a higher temperature slows the growth of some pathogens and speeds up immune responses", ["it kills all viruses at once", "it lowers the body's metabolic rate", "it stops sweating"], "Very high fevers are dangerous."),
    ("How do plants reduce water loss in drought?", "abscisic acid causes the stomata to close", ["auxin opens the stomata", "the plant makes more leaves", "the roots stop growing"], "Abscisic acid is a stress hormone."),
]
DIS = [
    ("What is a pathogen?", "an organism or agent that causes disease", ["any microorganism", "a white blood cell", "a toxin made by the body"], "Most microorganisms are harmless."),
    ("Which types of pathogens cause disease?", "viruses, bacteria, fungi, protists, parasites and prions", ["only bacteria", "only viruses", "only parasitic worms"], "Prions are misfolded proteins."),
    ("Why are antibiotics not used to treat viral infections?", "antibiotics target bacterial structures such as cell walls and ribosomes, which viruses do not have", ["viruses are too large", "antibiotics only work in plants", "viruses are not living, so they cannot be infected"], "Antivirals target viral processes."),
    ("How does antibiotic resistance develop?", "bacteria with resistance alleles survive antibiotic treatment and multiply", ["people become resistant to antibiotics", "antibiotics make bacteria change on purpose", "resistance comes from viruses only"], "Finishing courses and limiting use slow it."),
    ("What are Koch's postulates used for?", "showing that a particular microorganism causes a particular disease", ["making vaccines", "measuring blood glucose", "naming species"], "The pathogen must be isolated and cause the disease again."),
    ("Who showed that the bacterium Helicobacter pylori causes stomach ulcers?", "Australian scientists Barry Marshall and Robin Warren", ["Louis Pasteur", "Edward Jenner", "Alexander Fleming"], "They won the 2005 Nobel Prize."),
    ("Which is a vector-borne disease in Australia?", "Ross River virus, spread by mosquitoes", ["influenza", "tuberculosis", "tetanus"], "A vector carries the pathogen between hosts."),
    ("Which is part of the body's first line of defence?", "skin, mucus and stomach acid", ["antibodies", "memory B cells", "T cells"], "These are physical and chemical barriers."),
    ("What is the second line of defence?", "the non-specific innate response: inflammation, fever and phagocytes", ["antibodies only", "vaccination", "the skin"], "It responds to any pathogen."),
    ("What does the third line of defence involve?", "the specific adaptive response by B and T lymphocytes", ["the skin and mucus", "fever only", "stomach acid"], "It has memory."),
    ("What is an antigen?", "a molecule, usually on a pathogen's surface, recognised by the immune system", ["a protein made by B cells", "a white blood cell", "a type of antibiotic"], "Antibodies bind to antigens."),
    ("What do plasma cells make?", "antibodies", ["antigens", "histamine", "insulin"], "Plasma cells come from B lymphocytes."),
    ("What is the role of cytotoxic (killer) T cells?", "destroying body cells infected by viruses", ["making antibodies", "engulfing bacteria", "making mucus"], "Helper T cells activate B and cytotoxic T cells."),
    ("Why is the secondary immune response faster and stronger?", "memory cells made in the first response recognise the antigen quickly", ["the pathogen is weaker the second time", "antibodies never leave the blood", "the person has more skin"], "This is the basis of vaccination."),
    ("How does a vaccine work?", "it exposes the immune system to an antigen so memory cells form without causing the disease", ["it kills all bacteria in the body", "it gives the person antibodies for life", "it changes the person's DNA"], "This is artificial active immunity."),
    ("What is passive immunity?", "receiving antibodies made by another organism, such as from mother to baby", ["making your own antibodies after infection", "having memory cells", "being vaccinated"], "It gives short-term protection."),
    ("What is herd immunity?", "when enough people are immune, the spread of a pathogen is limited, protecting those who are not", ["immunity found only in cattle", "immunity from one infection", "a vaccine for animals"], "It protects babies and people who cannot be vaccinated."),
    ("What does the basic reproduction number R₀ tell epidemiologists?", "the average number of people one infected person infects in a fully susceptible population", ["the number of deaths from a disease", "the number of days a disease lasts", "the number of vaccines needed per person"], "If R is below 1, the outbreak shrinks."),
    ("What is an epidemic?", "a rapid increase in cases of a disease in a population or region", ["a disease found worldwide", "a disease that is always present at low levels", "an infection of one person"], "A pandemic is worldwide; an endemic disease is always present."),
    ("Which measure reduces the spread of a respiratory virus?", "hand washing, masks and staying home when sick", ["taking antibiotics", "eating more sugar", "sharing water bottles"], "These reduce transmission."),
    ("Which disease is caused by a prion?", "Creutzfeldt–Jakob disease (CJD)", ["malaria", "tuberculosis", "tinea"], "Prions are misfolded proteins with no DNA."),
    ("Which disease is caused by a fungus?", "tinea (athlete's foot)", ["influenza", "malaria", "tetanus"], "Fungi also cause many plant diseases."),
    ("Which disease is caused by a protist carried by mosquitoes?", "malaria (Plasmodium)", ["Ross River virus", "tetanus", "measles"], "Australia was declared malaria-free in 1981."),
    ("Which disease is caused by a bacterium?", "tuberculosis", ["measles", "influenza", "COVID-19"], "Bacteria can be treated with antibiotics."),
    ("What is the role of helper T cells?", "they release cytokines that activate B cells and cytotoxic T cells", ["they make antibodies", "they engulf bacteria", "they form the skin barrier"], "HIV destroys helper T cells."),
    ("What does an antibody do when it binds to a pathogen?", "it can clump pathogens together, neutralise toxins and mark them for phagocytes", ["it gives the pathogen energy", "it turns the pathogen into a virus", "it copies the pathogen's DNA"], "Each antibody fits one antigen."),
    ("What is inflammation?", "swelling, redness and heat as blood vessels widen and white blood cells move to an infected area", ["a type of antibody", "a vaccine reaction only", "the third line of defence"], "Mast cells release histamine."),
    ("What is quarantine?", "separating people or animals that may have been exposed to a disease until it is clear they are not infected", ["treating people with antibiotics", "making a vaccine", "cleaning water"], "Australia's border biosecurity uses quarantine."),
    ("Why is contact tracing used in an outbreak?", "to find and isolate people who may have been infected before they spread the disease", ["to count deaths", "to make antibodies", "to find the vector's DNA"], "It reduces transmission."),
    ("Why does Australia have strict biosecurity at its borders?", "to keep out pests and diseases, such as foot-and-mouth disease, that could harm people, farms and ecosystems", ["to stop all trade", "to make food cheaper", "because Australia has no diseases"], "Australia is free of many serious animal diseases."),
    ("What is a zoonosis?", "a disease that spreads from animals to people", ["a disease only of plants", "a disease of zoo keepers", "a type of vaccine"], "Hendra virus spreads from flying foxes via horses."),
    ("How do vaccines help eliminate a disease such as polio?", "high vaccination rates stop the pathogen spreading until it can no longer survive in the population", ["they cure people who already have it", "they kill the virus in the environment", "they change people's DNA"], "Smallpox was eradicated in 1980."),
    ("How do plants defend themselves against pathogens?", "waxy cuticles, thick cell walls and chemicals such as antimicrobial compounds", ["antibodies", "white blood cells", "fever"], "Some plants also close stomata or kill infected cells."),
]


def u1(X):
    return [
        ("DNA structure and replication", [(X.pool(DNA), 6), (X.ch("in_s12b", "molecular-basis-of-inheritance", 1), 8), (X.ch("in_s12b", "molecular-basis-of-inheritance", 3), 6)]),
        ("Genes and chromosomes", [(X.ch("al_bio", GI, 1, 12), 10), (X.pool(DNA), 6), (X.gen("gen_us_science_bio_dna_and_protein_synthesis", "g_comp"), 4)]),
        ("Transcription", [(X.ch("in_s12b", "molecular-basis-of-inheritance", 4), 14), (X.pool(DNA), 6)]),
        ("Translation and the genetic code", [(X.ch("al_bio", GI, 2, 12), 16), (X.pool(DNA), 4)]),
        ("Gene expression", [(X.ch("al_bio", GE, 2, 13, only=[0]), 10), (X.ch("al_bio", GI, 2, 12), 6), (X.pool(DNA), 4)]),
    ]


def u2(X):
    return [
        ("Meiosis and variation", [(X.ch("al_bio", GI, 3, 12, only=[0]), 10), (X.pool(INH), 6), (X.gen("gen_us_science_bio_meiosis_and_genetic_variation", "g_num"), 4)]),
        ("Monohybrid crosses", [(X.ch("al_bio", GP, 1, 13), 12), (X.ch("in_s12b", "principles-of-inheritance-and-variation", 1), 4), (X.pool(INH), 4)]),
        ("Dihybrid crosses and linkage", [(X.ch("in_s12b", "principles-of-inheritance-and-variation", 2), 16), (X.pool(INH), 4)]),
        ("Sex linkage and pedigrees", [(X.pool(INH), 6), (X.gen("gen_us_science_bio_punnett_squares_and_heredity", "g_xlink"), 4), (X.gen("gen_us_science_bio_punnett_squares_and_heredity", "g_blood"), 4), (X.ch("al_bio", GP, 1, 13), 6)]),
        ("The chi-squared test", [(X.ch("al_bio", GP, 2, 13), 20)]),
    ]


def u3(X):
    return [
        ("Mutations", [(X.pool(BIOT), 6), (X.ch("al_bio", GE, 1, 13), 10), (X.gen("gen_us_science_g8_genes_and_mutations", "g_type"), 4)]),
        ("Cutting and joining DNA", [(X.ch("al_bio", GE, 3, 13), 14), (X.pool(BIOT), 6)]),
        ("PCR", [(X.ch("al_bio", GE, 4, 13), 16), (X.pool(BIOT), 4)]),
        ("Gel electrophoresis and DNA profiling", [(X.ch("al_bio", GE, 5, 13), 16), (X.pool(BIOT), 4)]),
        ("Uses and ethics of biotechnology", [(X.pool(BIOT), 2), (X.ch("al_bio", GE, 2, 13), 12), (X.ch("al_bio", GE, 3, 13), 6)]),
    ]


def u4(X):
    return [
        ("Natural selection", [(X.pool(EVO), 6), (X.gen("gen_us_science_bio_natural_selection_and_adaptation", "g_resist"), 6), (X.gen("gen_us_science_bio_changes_in_trait_frequency", "g_freq"), 8)]),
        ("Allele frequencies and Hardy–Weinberg", [(X.ch("al_bio", GP, 3, 13), 16), (X.pool(EVO), 4)]),
        ("Genetic drift and gene flow", [(X.pool(EVO), 6), (X.ch("in_s12b", "evolution", 3), 8), (X.gen("gen_us_science_bio_changes_in_trait_frequency", "g_freq"), 6)]),
        ("Speciation", [(X.ch("al_bio", GP, 4, 13), 10), (X.gen("gen_us_science_bio_speciation_extinction_and_biodiversity", "g_iso"), 6), (X.pool(EVO), 4)]),
        ("Evidence for evolution", [(X.gen("gen_us_science_bio_evidence_for_evolution", "g_struct"), 8), (X.gen("gen_us_science_bio_evidence_for_evolution", "g_seq"), 8), (X.pool(EVO), 4)]),
    ]


def u5(X):
    return [
        ("Feedback and homeostasis", [(X.pool(HOME), 6), (X.gen("gen_us_science_bio_homeostasis_and_feedback", "g_loop"), 8), (X.ch("al_bio", RH, 1, 13), 6)]),
        ("Thermoregulation", [(X.pool(HOME), 14), (X.gen("gen_us_science_bio_homeostasis_and_feedback", "g_temp"), 4), (X.gen("gen_us_science_bio_homeostasis_and_feedback", "g_loop"), 2)]),
        ("Nerves and hormones", [(X.ch("al_bio", RH, 1, 13), 8), (X.ch("al_bio", RH, 2, 13), 8), (X.pool(HOME), 4)]),
        ("Blood glucose", [(X.ch("al_bio", RH, 3, 13), 16), (X.pool(HOME), 4)]),
        ("Water balance and the kidney", [(X.ch("al_bio", RH, 4, 13), 18), (X.pool(HOME), 2)]),
    ]


def u6(X):
    return [
        ("Pathogens and disease", [(X.pool(DIS), 6), (X.gen("gen_uk_science_y10_infection_and_response", "g_dis"), 10), (X.ch("in_s12b", "human-health-and-disease", 1), 4)]),
        ("Transmission and epidemiology", [(X.pool(DIS), 6), (X.gen("gen_uk_science_y10_infection_and_response", "g_grow"), 8), (X.gen("gen_uk_science_y10_infection_and_response", "g_zone"), 6)]),
        ("Innate and adaptive immunity", [(X.pool(DIS), 6), (X.ch("al_bio", "cells-and-the-immune-system", 5, 12), 8), (X.ch("in_s12b", "human-health-and-disease", 3), 6)]),
        ("Vaccines and herd immunity", [(X.pool(DIS), 6), (X.gen("gen_uk_science_y10_infection_and_response", "g_def"), 8), (X.ch("al_bio", "cells-and-the-immune-system", 5, 12), 6)]),
        ("Controlling disease", [(X.pool(DIS), 6), (X.ch("in_s12b", "human-health-and-disease", 2), 8), (X.src.B("gen_uk_science_y10_infection_and_response", "B5"), 6)]),
    ]


def UNITS():
    return [
        SR(BIO, 3, 1, "dna-genes-and-protein-synthesis", "DNA, genes and the continuity of life",
           "The structure of DNA and its replication; genes, chromosomes and the genetic code; transcription and translation in protein synthesis; introns, exons and gene regulation; how gene expression leads to differentiation.",
           "DNA, Genes and Protein Synthesis", "DNA, genes and protein synthesis",
           "Free Year 12 Biology worksheets on DNA and protein synthesis: base pairing, replication, the genetic code, transcription, translation, codons, anticodons and gene expression. 100 questions with answers.",
           "DNA → (transcription) → mRNA → (translation) → protein.", "A pairs with T (U in RNA); C pairs with G.",
           "<p>DNA is a double helix of nucleotides; A pairs with T and C with G. Replication is semi-conservative. A <b>gene</b> is a DNA sequence that codes for a protein.</p>"
           "<p>In <b>transcription</b>, RNA polymerase makes mRNA from the template strand (U replaces T); introns are removed. In <b>translation</b>, ribosomes read mRNA codons and tRNA anticodons bring the amino acids. Cells with the same DNA differ because they express different genes.</p>",
           [("Template strand TAC GGA TTC. mRNA?", ["complementary bases, U for A"], "AUG CCU AAG"),
            ("mRNA AUG CCU AAG: how many amino acids?", ["3 codons"], "3 amino acids")],
           ["Writing T instead of U in mRNA.", "Saying genes are made of protein.", "Mixing up codons (mRNA) and anticodons (tRNA)."],
           [("Why is the genetic code called universal?", "Almost all organisms use the same codons for the same amino acids, which is why a human gene can be expressed in bacteria."),
            ("Where do transcription and translation happen in eukaryotes?", "Transcription in the nucleus; translation on ribosomes in the cytoplasm or on the rough endoplasmic reticulum.")],
           u1),
        SR(BIO, 3, 2, "cell-division-and-inheritance", "DNA, genes and the continuity of life",
           "Meiosis and the sources of genetic variation; alleles, genotype and phenotype; monohybrid and dihybrid crosses; dominance, codominance and incomplete dominance; sex linkage and pedigrees; the chi-squared test.",
           "Meiosis, Inheritance and Genetic Crosses", "cell division and inheritance",
           "Free Year 12 Biology worksheets on inheritance: meiosis, crossing over, alleles, Punnett squares, dihybrid crosses, codominance, sex linkage, pedigrees and the chi-squared test. 100 questions with answers.",
           "Aa × Aa → 3 dominant : 1 recessive.", "Sex-linked recessive traits are more common in males (XY).",
           "<p>Meiosis makes haploid gametes; crossing over and independent assortment produce new combinations of alleles. The <b>genotype</b> (alleles) with the environment gives the <b>phenotype</b>.</p>"
           "<p>Use Punnett squares for crosses: Aa × Aa gives 3 : 1; AaBb × AaBb gives 9 : 3 : 3 : 1 (unless genes are linked). In codominance both alleles show (blood group AB). X-linked recessive traits appear more in males. The chi-squared test checks if observed ratios fit expected ones.</p>",
           [("Bb × bb: proportion bb?", ["Bb × bb gives Bb, Bb, bb, bb"], "1/2"),
            ("Carrier mother XᴴXʰ × normal father XᴴY. Chance a son has haemophilia?", ["sons get X from mother: Xᴴ or Xʰ"], "1/2")],
           ["Thinking dominant means more common.", "Forgetting that sons get their X chromosome from their mother.", "Using a 3 : 1 ratio for a test cross: it gives 1 : 1."],
           [("How does meiosis cause variation?", "Crossing over swaps sections between homologous chromosomes, and independent assortment shuffles which chromosome of each pair goes into a gamete."),
            ("What does a chi-squared test tell you?", "Whether the difference between observed and expected numbers is small enough to be due to chance (compare χ² with the critical value).")],
           u2),
        SR(BIO, 3, 3, "mutations-and-biotechnology", "DNA, genes and the continuity of life",
           "Point and chromosomal mutations and their effects; mutagens; restriction enzymes, ligase and recombinant DNA; PCR; gel electrophoresis and DNA profiling; gene editing with CRISPR; uses and ethics of biotechnology.",
           "Mutations, PCR and Biotechnology", "mutations and biotechnology",
           "Free Year 12 Biology worksheets on mutations and biotechnology: point and frameshift mutations, restriction enzymes, plasmids, PCR, gel electrophoresis, DNA profiling, CRISPR and GMOs. 100 questions with answers.",
           "PCR doubles DNA each cycle: 2ⁿ copies after n cycles.", "In a gel, small fragments move further.",
           "<p>Mutations change the DNA sequence. A substitution may change one amino acid (or none: silent); an insertion or deletion shifts the reading frame. Mutations are the source of new alleles.</p>"
           "<p>Gene technology uses <b>restriction enzymes</b> to cut DNA and <b>ligase</b> to join it, for example into a plasmid. <b>PCR</b> copies DNA (2ⁿ copies after n cycles). <b>Gel electrophoresis</b> separates fragments by size, as in DNA profiling. CRISPR-Cas9 edits a chosen sequence.</p>",
           [("1 DNA molecule, 10 PCR cycles. Copies?", ["2¹⁰"], "1024"),
            ("3000 bp DNA cut at 1200. Fragments?", ["1200 and 3000 − 1200"], "1200 bp and 1800 bp")],
           ["Thinking all mutations are harmful.", "Saying larger DNA fragments move further in a gel.", "Forgetting that PCR needs primers and a heat-stable polymerase."],
           [("Why is a frameshift mutation usually worse than a substitution?", "It changes every codon after the mutation, so many amino acids change and a stop codon may appear early."),
            ("How is DNA profiling used?", "Short tandem repeats are copied by PCR and separated by size; the pattern of bands identifies people for forensics and paternity testing.")],
           u3),
        SR(BIO, 3, 4, "evolution-and-population-genetics", "Continuity of life on Earth",
           "Genetic variation and natural selection; gene pools and allele frequencies; the Hardy–Weinberg principle; genetic drift, founder effect, bottlenecks and gene flow; speciation and reproductive isolation; evidence for evolution.",
           "Evolution, Natural Selection and Speciation", "evolution and population genetics",
           "Free Year 12 Biology worksheets on evolution: natural selection, allele frequencies, Hardy–Weinberg, genetic drift, the founder effect, gene flow, speciation and evidence for evolution. 100 questions with answers.",
           "Evolution is a change in allele frequencies in a gene pool.", "p + q = 1 and p² + 2pq + q² = 1.",
           "<p>Natural selection acts on heritable variation: individuals with favourable alleles survive and reproduce more, so those alleles increase. <b>Genetic drift</b> (chance, strongest in small populations), the <b>founder effect</b>, <b>bottlenecks</b> and <b>gene flow</b> also change allele frequencies.</p>"
           "<p>When populations are isolated (for example by Bass Strait) and diverge until they can no longer interbreed, new species form. Evidence for evolution includes fossils, comparative anatomy, embryology, biogeography and DNA comparisons.</p>",
           [("q² = 0.09. Find q and the carrier frequency.", ["q = 0.3, p = 0.7", "2pq = 2 × 0.7 × 0.3"], "0.42"),
            ("A ring of 10 survivors founds a new population. Which effect?", ["a few individuals start a population"], "the founder effect")],
           ["Saying individuals evolve: populations do.", "Thinking organisms change because they need to.", "Using q² as the carrier frequency."],
           [("What are the conditions for Hardy–Weinberg equilibrium?", "A large population, random mating, no mutation, no migration and no selection. Real populations rarely meet them, so frequencies change."),
            ("Why is Australian wildlife so useful for studying evolution?", "Long isolation produced adaptive radiation of marsupials and convergent evolution with placental mammals elsewhere.")],
           u4),
        SR(BIO, 4, 5, "homeostasis", "Homeostasis",
           "The stimulus–response model and negative feedback; thermoregulation in endotherms and ectotherms; the nervous and endocrine systems; blood glucose regulation by insulin and glucagon; water balance, ADH and the kidney; plant responses and hormones.",
           "Homeostasis: Temperature, Glucose and Water Balance", "homeostasis",
           "Free Year 12 Biology worksheets on homeostasis: negative feedback, thermoregulation, nerves and hormones, insulin and glucagon, ADH, the kidney and plant hormones. 100 questions with answers.",
           "Stimulus → receptor → control centre → effector → response.", "Negative feedback brings a variable back to its set point.",
           "<p>Homeostasis keeps the internal environment stable. A change (stimulus) is detected by receptors; a control centre (often the hypothalamus) sends signals by nerves or hormones to effectors, which reverse the change: <b>negative feedback</b>.</p>"
           "<p>Body temperature is controlled by sweating, shivering and changes to skin blood flow. Insulin lowers and glucagon raises blood glucose. ADH controls how much water the kidneys reabsorb. Australian animals such as red kangaroos and hopping mice show special adaptations.</p>",
           [("Blood glucose rises after a meal. Which hormone and gland?", ["detected by the pancreas", "beta cells release insulin"], "insulin from the pancreas"),
            ("Filtrate 125 mL/min, urine 1 mL/min. % reabsorbed?", ["(125 − 1) ÷ 125 × 100"], "99.2%")],
           ["Saying negative feedback is bad: it is stabilising.", "Mixing up glucagon (hormone) with glycogen (store).", "Thinking ADH makes more urine: it makes less, more concentrated urine."],
           [("Why is the hypothalamus important?", "It is the control centre for temperature and water balance and links the nervous and endocrine systems through the pituitary gland."),
            ("How do ectotherms control their temperature?", "Mostly by behaviour: basking in sun, moving to shade, burrowing or changing their body position.")],
           u5),
        SR(BIO, 4, 6, "infectious-disease-and-immunity", "Infectious disease",
           "Pathogens (viruses, bacteria, fungi, protists, parasites, prions) and how they cause disease; transmission and vectors; Koch's postulates; innate and adaptive immunity; antibodies, B and T cells; vaccination and herd immunity; epidemiology and controlling outbreaks.",
           "Infectious Disease and the Immune System", "infectious disease and immunity",
           "Free Year 12 Biology worksheets on infectious disease: pathogens, transmission, vectors, the three lines of defence, B and T cells, antibodies, vaccines, herd immunity and antibiotic resistance. 100 questions with answers.",
           "Three lines of defence: barriers, innate response, adaptive response.", "Memory cells make the second response faster and stronger.",
           "<p>Pathogens include viruses, bacteria, fungi, protists, parasites and prions. They spread by direct contact, droplets, food and water, or vectors such as mosquitoes (Ross River virus).</p>"
           "<p>The body's defences: (1) barriers such as skin and mucus; (2) the innate response (inflammation, fever, phagocytes); (3) the adaptive response, in which B cells make antibodies and T cells kill infected cells and make memory cells. Vaccines create memory without disease; high vaccination rates give herd immunity.</p>",
           [("R₀ = 3. How many people infected after 3 generations from 1 case?", ["1 → 3 → 9 → 27"], "27 new cases in the third generation"),
            ("A newborn gets antibodies in breast milk. Type of immunity?", ["antibodies made by another person", "no memory cells"], "natural passive immunity")],
           ["Using antibiotics for a viral infection.", "Saying a vaccine contains antibodies: it contains antigens.", "Thinking people become resistant to antibiotics: bacteria do."],
           [("What is the difference between active and passive immunity?", "Active: your own immune system makes antibodies and memory cells (after infection or vaccination). Passive: you receive ready-made antibodies, so protection is short."),
            ("Why do some vaccines need boosters?", "Memory cell numbers and antibody levels fall over time, or the pathogen changes (as with influenza), so a booster renews protection.")],
           u6),
    ]
