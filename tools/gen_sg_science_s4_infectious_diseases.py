# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Biology (6093), Topic 9: Infectious Diseases in Humans
  python tools/gen_sg_science_s4_infectious_diseases.py
Pathogens (bacteria and viruses); influenza and pneumococcal disease as examples of infectious diseases (cause, transmission,
symptoms, prevention); the body's defences (skin, mucus and cilia, stomach acid, blood clotting, phagocytosis, antibodies made by
lymphocytes); active and passive immunity; vaccination and herd immunity; antibiotics and antibiotic resistance.
UK KS4 infection makers are reused (Singapore names; plant diseases dropped); the rest is written here.
Wrong answers come from real mistakes: "antibiotics kill viruses", "a vaccine contains antibodies", "bacteria become immune to
antibiotics", "influenza is caused by bacteria", "white blood cells eat viruses only".
"""
from sg_ol import OL, seed_of, make_ol, tq, rows, pool

LV, SUBJ, SORT = 4, "Biology", 17
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_def = src("gen_uk_science_y10_infection_and_response", "g_def")
uk_grow = src("gen_uk_science_y10_infection_and_response", "g_grow")
uk_zone = src("gen_uk_science_y10_infection_and_response", "g_zone")

DIS = {"influenza": ("a virus", "droplets from coughs and sneezes, and touching contaminated surfaces", "fever, cough, sore throat, muscle aches and tiredness",
                     "a yearly influenza vaccine, covering the nose and mouth when coughing, and washing hands"),
       "pneumococcal disease": ("a bacterium (Streptococcus pneumoniae)", "droplets from the nose and throat of an infected person", "fever and chest pain; it can cause pneumonia, meningitis and blood infections",
                                "the pneumococcal vaccine and good hygiene; it is treated with antibiotics")}


def g_dis():
    d = R.choice(sorted(DIS))
    other = [x for x in DIS if x != d][0]
    cause, trans, sym, prev = DIS[d]
    k = R.choice(["cause", "trans", "sym", "prev"])
    o = DIS[other]
    if k == "cause":
        return tq("What causes %s?" % d, cause, [o[0], "a fungus", "a lack of vitamin C"], "Influenza is viral; pneumococcal disease is bacterial.")
    if k == "trans":
        return tq("How is %s mainly spread?" % d, trans, ["bites from infected mosquitoes", "drinking contaminated water", "eating undercooked chicken"], "Both are spread by droplets from the airways.")
    if k == "sym":
        return tq("Which symptoms are typical of %s?" % d, sym, [o[2], "a red rash and itching only", "bleeding gums and loose teeth"], "Learn the main symptoms of each disease.")
    return tq("Which measures help to prevent or control %s?" % d, prev, [o[3], "taking antibiotics for every cold", "drinking sugary drinks"], "Vaccination and hygiene reduce spread.")


PATH = [("influenza", "a virus"), ("the common cold", "a virus"), ("COVID-19", "a virus"), ("dengue fever", "a virus"),
        ("pneumococcal disease", "a bacterium"), ("tuberculosis", "a bacterium"), ("cholera", "a bacterium"), ("tetanus", "a bacterium")]


def g_path():
    d, t = R.choice(PATH)
    if R.random() < 0.5:
        return tq("What type of pathogen causes %s?" % d, t, [x for x in ("a virus", "a bacterium", "a fungus", "not a pathogen (a deficiency)") if x != t],
                  "Antibiotics can treat bacterial diseases, but not viral ones.")
    a = "yes" if t == "a bacterium" else "no"
    return tq("Can %s be treated with antibiotics?" % d, a, ["no" if a == "yes" else "yes", "only if a vaccine is also given", "only in children"],
              "%s is caused by %s. Antibiotics kill bacteria but have no effect on viruses." % (d[0].upper() + d[1:], t))


IMM = [("You have chickenpox and recover, and do not catch it again.", "natural active immunity"),
       ("You receive the influenza vaccine.", "artificial active immunity"),
       ("A baby receives antibodies from its mother through breast milk.", "natural passive immunity"),
       ("A person bitten by a snake is given an injection of ready-made antibodies (antivenom).", "artificial passive immunity"),
       ("A fetus receives antibodies across the placenta.", "natural passive immunity"),
       ("A child is given the pneumococcal vaccine.", "artificial active immunity"),
       ("A person recovers from influenza and makes memory cells.", "natural active immunity"),
       ("A patient exposed to tetanus is injected with antibodies against the tetanus toxin.", "artificial passive immunity"),
       ("A student catches measles as a child and is protected for life.", "natural active immunity"),
       ("A newborn baby is protected for a few months by antibodies that crossed the placenta from its mother.", "natural passive immunity"),
       ("A traveller is given a hepatitis A vaccine before a trip.", "artificial active immunity"),
       ("A nurse is given a booster dose of the tetanus vaccine.", "artificial active immunity"),
       ("A patient with a dangerous infection is given a serum of antibodies from a donor.", "artificial passive immunity"),
       ("A baby drinks colostrum, the first breast milk, rich in antibodies.", "natural passive immunity"),
       ("A man catches COVID-19, recovers and has antibodies months later.", "natural active immunity"),
       ("A health worker is injected with ready-made antibodies after a needle-stick injury.", "artificial passive immunity")]


TRANS = [("dengue fever", "bites from infected Aedes mosquitoes"), ("cholera", "drinking water contaminated with faeces"), ("tuberculosis", "breathing in droplets from an infected person's cough"),
         ("tetanus", "bacteria in soil entering a deep wound"), ("influenza", "droplets from coughs and sneezes"), ("food poisoning", "eating food contaminated with bacteria")]
g_trans = rows(R, TRANS, "How is %s mainly transmitted?", "Which disease is mainly spread by %s?")


def g_imm():
    sit, a = R.choice(IMM)
    return tq("%s Which type of immunity is this?" % sit, a, [x for x in ("natural active immunity", "artificial active immunity", "natural passive immunity", "artificial passive immunity") if x != a],
              "Active: the body makes its own antibodies and memory cells (long-lasting). Passive: ready-made antibodies are given (short-lived).")


DEF = [("the skin", "a physical barrier that stops pathogens entering"), ("mucus and cilia in the airways", "trap pathogens and sweep them up to the throat"),
       ("hydrochloric acid in the stomach", "kills many pathogens in food and drink"), ("blood clotting", "seals wounds so pathogens cannot enter"),
       ("phagocytes", "engulf and digest pathogens"), ("lymphocytes", "make antibodies specific to the antigens on a pathogen")]
g_defs = rows(R, DEF, "What role does %s play in defending the body against pathogens?", "Which defence has this role: “%s”?")


def g_ab():
    k = R.choice(["agg", "lys", "neu", "mark"])
    acts = {"agg": "cause pathogens to clump together (agglutination)", "lys": "break open the cell walls of bacteria", "neu": "neutralise toxins made by bacteria",
            "mark": "attach to pathogens, making them easier for phagocytes to engulf"}
    a = acts[k]
    return tq("Which is one way antibodies help to destroy pathogens? They…", a, ["digest the pathogen inside the lymphocyte", "carry oxygen to the pathogen", "turn the pathogen into a vaccine"],
              "Antibodies are proteins made by lymphocytes. They %s, among other actions." % a)


POOL1 = pool(R, [
    ("What is a pathogen?", "a microorganism that causes disease", ["any microorganism", "a white blood cell", "an antibody"], "Bacteria and viruses are pathogens."),
    ("What is an antigen?", "a molecule on the surface of a pathogen that triggers the making of antibodies", ["a protein made by lymphocytes", "a drug that kills bacteria", "a type of white blood cell"], "Each pathogen has its own antigens."),
    ("What does a vaccine contain?", "dead or weakened pathogens, or their antigens", ["antibodies", "antibiotics", "white blood cells"], "It triggers an immune response without causing the disease."),
    ("Why does a vaccinated person not become ill when infected?", "Memory cells make antibodies quickly, before the pathogen can multiply.", ["The vaccine kills all pathogens in the air.", "The person has no lymphocytes.", "The vaccine stays in the blood for ever as antibodies."], "The secondary response is faster and larger."),
    ("Why do antibiotics not work against influenza?", "Influenza is caused by a virus, and antibiotics act only on bacteria.", ["Influenza is too mild.", "Antibiotics are too slow.", "Influenza bacteria are resistant."], "Antiviral drugs are different."),
    ("What is herd immunity?", "When most people are vaccinated, the disease cannot spread easily, protecting those who are not immune.", ["Animals cannot catch human diseases.", "Everyone is born immune.", "Only farm workers are vaccinated."], "This protects babies and people who cannot be vaccinated."),
    ("Why must a new influenza vaccine be made each year?", "The virus mutates, so its antigens change.", ["The old vaccine stops working in the fridge.", "People lose all their lymphocytes.", "Influenza becomes a bacterium."], "Memory cells may not recognise the new antigens."),
    ("Which cells make antibodies?", "lymphocytes", ["phagocytes", "red blood cells", "platelets"], "Phagocytes engulf pathogens."),
    ("Why should a patient finish the whole course of antibiotics?", "to kill all the bacteria, so resistant ones are less likely to survive and multiply", ["so the body makes antibodies", "to kill viruses as well", "because antibiotics are vaccines"], "Stopping early can leave the toughest bacteria alive."),
    ("How do antibiotic-resistant bacteria arise?", "A random mutation makes some bacteria resistant; they survive the antibiotic and multiply.", ["Bacteria choose to become immune.", "Antibiotics turn bacteria into viruses.", "The patient becomes resistant to the antibiotic."], "This is natural selection."),
])
POOL5 = pool(R, [
    ("A graph shows antibody levels after a first and second dose of a vaccine. Why is the second response faster and higher?", "Memory cells from the first dose recognise the antigen and make antibodies quickly.", ["The second dose contains antibodies.", "The person has more red blood cells.", "The pathogen is weaker the second time."], "This is the basis of booster doses."),
    ("Why is passive immunity short-lived?", "The antibodies given are broken down and no memory cells are made.", ["The person makes too many antibodies.", "The antibodies multiply.", "The pathogens are all killed at once."], "Active immunity lasts much longer."),
    ("Why are elderly people in Singapore encouraged to receive the pneumococcal vaccine?", "They are more likely to develop serious pneumonia from the infection.", ["The disease affects only the elderly.", "The vaccine cures arthritis.", "Antibiotics do not exist for this disease."], "It is part of the national adult immunisation schedule."),
    ("Why does overuse of antibiotics in farming worry doctors?", "It increases the chance of antibiotic-resistant bacteria spreading to humans.", ["It makes animals immune to viruses.", "It uses up vaccines.", "It makes food taste bitter."], "Resistant bacteria are harder to treat."),
    ("Why do doctors not give antibiotics for the common cold?", "It is caused by a virus, and unnecessary antibiotics encourage resistance.", ["Colds are caused by fungi.", "Antibiotics make colds last longer only in adults.", "Colds cannot be passed on."], "Rest and fluids are recommended."),
    ("How does wearing a mask reduce the spread of influenza?", "It stops many droplets from the nose and mouth spreading to others.", ["It kills viruses in the blood.", "It makes the wearer immune.", "It replaces vaccination."], "Hand washing also helps."),
    ("A person cuts a finger, and the wound becomes red and swollen. Which cells move to the area to engulf bacteria?", "phagocytes", ["red blood cells", "platelets", "nerve cells"], "This is part of the inflammatory response."),
    ("Why is a vaccine said to have “no risk of causing the disease” when it contains weakened pathogens?", "The weakened pathogens cannot multiply fast enough to cause illness but still carry the antigens.", ["The vaccine contains antibiotics.", "The pathogens are alive and dangerous.", "It contains no antigens."], "In rare cases mild symptoms occur."),
])


def main():
    sets = U.sets([
        ("Pathogens and infectious diseases", [(g_dis, 6), (g_path, 8), (POOL1, 3), (g_trans, 3)]),
        ("The body's defences", [(g_defs, 8), (uk_def, 7), (g_ab, 3), (POOL1, 2)]),
        ("Immunity and vaccination", [(g_imm, 10), (POOL1, 3), (POOL5, 3), (g_trans, 2), (g_ab, 1), (g_dis, 1)]),
        ("Antibiotics", [(uk_zone, 7), (uk_grow, 6), (g_path, 4), (POOL1, 2), (POOL5, 1)]),
        ("Exam-style questions", [(POOL5, 4), (g_imm, 4), (g_trans, 3), (uk_zone, 2), (uk_grow, 3), (g_defs, 2), (g_dis, 1), (uk_def, 1)]),
    ])
    make_ol(LV, SUBJ, "infectious-diseases", SORT, "Infectious Diseases in Humans",
            "Describe infectious diseases as caused by pathogens such as bacteria and viruses, using influenza and pneumococcal disease as examples, including "
            "their causes, transmission and symptoms; describe the body's defences, including physical barriers, phagocytosis and the production of antibodies by "
            "lymphocytes; distinguish between active and passive immunity; describe how vaccination works and the role of herd immunity; explain why antibiotics "
            "kill bacteria but not viruses and how antibiotic resistance develops (summary of the Singapore-Cambridge O-Level Biology 6093 syllabus).",
            "Infectious Diseases in Humans", "Infectious diseases",
            "Free Secondary 4 O-Level Biology worksheets on infectious diseases: pathogens, influenza, pneumococcal disease, body defences, antibodies, immunity, "
            "vaccines and antibiotics. 100 questions with answers.",
            "Vaccines make memory cells; antibiotics kill bacteria, not viruses.", "Active immunity: your own antibodies. Passive: ready-made antibodies.",
            "<p><b>The body fights pathogens in layers.</b></p><ul>"
            "<li>Barriers: skin, mucus and cilia, stomach acid, blood clotting.</li>"
            "<li>Phagocytes engulf pathogens; lymphocytes make antibodies specific to antigens and leave memory cells.</li>"
            "<li>Vaccines contain weakened or dead pathogens or antigens. They give active immunity without the disease.</li>"
            "<li>Antibiotics kill bacteria but not viruses. Overuse lets resistant bacteria survive and spread.</li></ul>",
            [("Baby gets antibodies in breast milk.", ["ready-made antibodies", "no memory cells"], "natural passive immunity"),
             ("Antibiotic for influenza?", ["influenza is a virus"], "no effect")],
            ["Saying antibiotics kill viruses.", "Saying a vaccine contains antibodies.", "Saying bacteria “become immune” to antibiotics.",
             "Mixing up active and passive immunity."],
            [("How does a vaccine work?", "It contains dead or weakened pathogens or their antigens. Lymphocytes make antibodies and memory cells, so if the real pathogen enters later, antibodies are made quickly before illness develops."),
             ("What is the difference between active and passive immunity?", "In active immunity the body makes its own antibodies and memory cells, so it lasts a long time. In passive immunity ready-made antibodies are received, so it acts at once but lasts only a short time."),
             ("Why do antibiotics not work on viruses?", "Antibiotics damage structures or processes found in bacteria, such as cell walls. Viruses do not have these and reproduce inside host cells.")],
            sets)


if __name__ == "__main__":
    main()
