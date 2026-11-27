# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Biology (6093), Topic 4: Nutrition in Humans
  python tools/gen_sg_science_s3_nutrition_in_humans.py
The alimentary canal and its parts; ingestion, digestion, absorption, assimilation and egestion; mechanical digestion (teeth,
peristalsis) and chemical digestion (amylase, maltase, proteases, lipase, the role of bile); absorption in the small intestine
and the structure of villi; the hepatic portal vein and the roles of the liver (glycogen storage, deamination, breaking down
alcohol and toxins, bile).
UK KS3 digestion makers are reused (Singapore names); the rest is written here.
Wrong answers come from real mistakes: "bile is an enzyme", "digestion of protein starts in the mouth", "most absorption happens
in the stomach", "the large intestine digests food", "villi increase the volume of the small intestine".
"""
from sg_ol import OL, seed_of, make_ol, tq, rows, pool

LV, SUBJ, SORT = 3, "Biology", 22
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_enz = src("gen_uk_science_y8_food_and_digestion", "g_enz")

PART = [("the mouth", "chewing (mechanical digestion) and the start of starch digestion by salivary amylase"),
        ("the oesophagus", "carrying food to the stomach by peristalsis"),
        ("the stomach", "churning food and starting protein digestion with pepsin in hydrochloric acid"),
        ("the duodenum", "receiving pancreatic juice and bile, where digestion of starch, protein and fat continues"),
        ("the ileum", "completing digestion and absorbing digested food through its villi"),
        ("the colon", "absorbing water and mineral salts from undigested food"),
        ("the rectum", "storing faeces before egestion"),
        ("the pancreas", "making pancreatic juice containing amylase, trypsin and lipase"),
        ("the liver", "making bile, storing glycogen and carrying out deamination"),
        ("the gall bladder", "storing bile and releasing it into the duodenum")]
g_part = rows(R, PART, "What is the main function of %s?", "Which part of the digestive system is responsible for %s?")

ENZ = [("salivary amylase", "starch", "maltose", "the mouth"), ("pancreatic amylase", "starch", "maltose", "the small intestine"),
       ("maltase", "maltose", "glucose", "the small intestine"), ("pepsin", "protein", "polypeptides", "the stomach"),
       ("trypsin", "protein", "polypeptides", "the small intestine"), ("peptidase (erepsin)", "peptides", "amino acids", "the small intestine"),
       ("lipase", "fats", "fatty acids and glycerol", "the small intestine")]


def g_enz():
    e, sub, prod, where = R.choice(ENZ)
    k = R.choice(["sub", "prod", "where", "which"])
    o = [x for x in ENZ if x[0] != e]
    if k == "sub":
        w = sorted({x[1] for x in o if x[1] != sub})
        return tq("Which substance does %s digest?" % e, sub, R.sample(w, 3), "%s digests %s into %s." % (e[0].upper() + e[1:], sub, prod))
    if k == "prod":
        w = sorted({x[2] for x in o if x[2] != prod})
        return tq("What is the product of digestion by %s?" % e, prod, R.sample(w, 3), "%s digests %s into %s." % (e[0].upper() + e[1:], sub, prod))
    if k == "where":
        w = [x for x in ("the mouth", "the stomach", "the small intestine", "the large intestine") if x != where]
        return tq("Where does %s act?" % e, where, w, "%s acts in %s." % (e[0].upper() + e[1:], where))
    w = sorted({x[0] for x in o if x[1] != sub and x[2] != prod})
    if len(w) < 3:
        return None
    return tq("Which enzyme digests %s into %s?" % (sub, prod), e, R.sample(w, 3), "Each enzyme is specific to its substrate.")


STEP = [("ingestion", "taking food into the mouth"), ("digestion", "breaking down large, insoluble food molecules into small, soluble molecules"),
        ("absorption", "the movement of digested food molecules from the small intestine into the blood or lymph"),
        ("assimilation", "the use of absorbed food molecules by body cells"), ("egestion", "the removal of undigested food as faeces through the anus"),
        ("peristalsis", "waves of muscle contraction that push food along the alimentary canal"),
        ("emulsification", "breaking large fat droplets into small droplets, increasing the surface area for lipase")]
g_step = rows(R, STEP, "What is meant by %s?", "Which process is %s?")

VIL = [("many villi and microvilli", "a very large surface area for absorption"), ("a wall only one cell thick", "a short distance for diffusion"),
       ("a dense network of blood capillaries", "a steep concentration gradient, as absorbed food is carried away"),
       ("a lacteal in each villus", "absorption of fatty acids and glycerol into the lymph"), ("a long small intestine (about 6 m)", "plenty of time for absorption"),
       ("many mitochondria in the epithelial cells", "energy for active transport of glucose and amino acids")]
g_vil = rows(R, VIL, "How does %s help absorption in the small intestine?", "Which feature of the small intestine gives %s?")

LIV = [("excess glucose", "is converted into glycogen and stored"), ("excess amino acids", "are deaminated: the amino group becomes urea"),
       ("alcohol", "is broken down by enzymes, but too much damages liver cells (cirrhosis)"), ("old red blood cells", "are broken down; iron is stored and bile pigments are made"),
       ("hormones such as insulin and glucagon", "act on the liver to control the glucose level in the blood")]
g_liv = rows(R, LIV, "What happens to %s in the liver?", "In the liver, which substance %s?")

POOL1 = pool(R, [
    ("Why must food be digested?", "Large, insoluble molecules must be broken into small, soluble ones that can be absorbed.", ["to make food larger", "to kill all bacteria", "to remove water"], "Starch → glucose, protein → amino acids, fat → fatty acids and glycerol."),
    ("What is the role of hydrochloric acid in the stomach?", "It gives the acidic pH needed by pepsin and kills many bacteria.", ["It digests starch.", "It emulsifies fats.", "It neutralises bile."], "The stomach pH is about 2."),
    ("What does bile do?", "It emulsifies fats and neutralises acidic chyme from the stomach.", ["It digests protein.", "It digests starch into maltose.", "It absorbs water."], "Bile contains no enzymes."),
    ("Where is most water absorbed?", "in the small intestine, with the rest absorbed in the colon", ["in the stomach", "in the mouth", "in the oesophagus"], "The colon absorbs the remaining water."),
    ("Which blood vessel carries absorbed food from the small intestine to the liver?", "the hepatic portal vein", ["the hepatic artery", "the aorta", "the pulmonary vein"], "The liver controls what enters the general circulation."),
    ("Why does the stomach have a thick, muscular wall?", "to churn food and mix it with gastric juice", ["to absorb glucose", "to make bile", "to store faeces"], "Mechanical digestion."),
    ("Which teeth are used for cutting food?", "incisors", ["molars", "premolars", "canines"], "Molars grind food."),
    ("Why does chewing help digestion?", "It breaks food into smaller pieces, increasing the surface area for enzymes.", ["It digests protein.", "It makes the food more acidic.", "It absorbs the food."], "Mechanical digestion."),
    ("What is deamination?", "removal of the amino group from excess amino acids in the liver, forming urea", ["absorption of amino acids", "building proteins from amino acids", "breaking down fats"], "Urea is excreted by the kidneys."),
    ("What does the pancreas release into the duodenum?", "pancreatic juice containing amylase, trypsin and lipase", ["bile", "hydrochloric acid", "saliva"], "Pancreatic juice is alkaline."),
])
POOL5 = pool(R, [
    ("A person has their gall bladder removed. Which food would they find hardest to digest?", "fatty food", ["starchy food", "sugary drinks", "lean meat"], "Less bile is released to emulsify fat."),
    ("Starch solution and amylase are mixed at 37 °C. After 10 minutes iodine stays orange-brown. What does this show?", "All the starch has been digested.", ["The amylase is denatured.", "Starch is still present.", "Iodine does not react with starch."], "Amylase digests starch to maltose."),
    ("Why does pepsin not digest protein in the small intestine?", "The small intestine is alkaline, but pepsin needs an acidic pH.", ["There is no protein there.", "Pepsin is digested by amylase.", "The small intestine is too warm."], "Each enzyme has an optimum pH."),
    ("Why does a person with a damaged ileum lose weight?", "Less digested food is absorbed because the villi are damaged.", ["They digest food faster.", "They make more bile.", "They absorb more water."], "Absorption needs a large surface area."),
    ("Fatty acids are absorbed into which part of a villus?", "the lacteal", ["the blood capillaries only", "the hepatic artery", "the goblet cells"], "They travel in the lymph."),
    ("Why does drinking too much alcohol over many years damage the liver?", "Liver cells are damaged as they break down alcohol, leading to cirrhosis.", ["Alcohol is stored as glycogen.", "Alcohol is converted to urea.", "The liver absorbs alcohol into bile."], "The liver can no longer function well."),
    ("Visking tubing containing starch and amylase is placed in water at 37 °C. After 30 minutes, which substance is found in the water?", "maltose (reducing sugar)", ["starch", "amylase", "protein"], "Small maltose molecules pass through the tubing; starch and enzyme do not."),
    ("A meal contains starch. Where are the products of its digestion first absorbed into the blood?", "in the ileum (small intestine)", ["in the stomach", "in the colon", "in the mouth"], "Glucose is absorbed through the villi."),
    ("After absorption, glucose reaches the liver before the rest of the body. Why is this useful?", "The liver can store excess glucose as glycogen and keep the blood glucose level steady.", ["The liver turns all glucose into urea.", "The liver digests glucose.", "Glucose is needed only by the liver."], "The hepatic portal vein leads to the liver."),
    ("Which shows the correct order of processes for food?", "ingestion → digestion → absorption → assimilation → egestion", ["digestion → ingestion → absorption → egestion → assimilation", "ingestion → absorption → digestion → assimilation → egestion", "ingestion → digestion → egestion → absorption → assimilation"], "Undigested food is egested last."),
    ("Why does the duodenum need an alkaline environment?", "Pancreatic enzymes such as trypsin and lipase work best at a slightly alkaline pH.", ["Pepsin works best there.", "Alkali digests fat.", "Alkali kills all bacteria."], "Bile and pancreatic juice neutralise the stomach acid."),
    ("Which statement about digestion of fat is correct?", "Bile emulsifies fat and lipase digests it into fatty acids and glycerol.", ["Bile digests fat into glycerol.", "Lipase emulsifies fat.", "Fat is digested in the mouth."], "Bile is not an enzyme."),
])


def main():
    sets = U.sets([
        ("The alimentary canal", [(g_part, 10), (g_step, 6), (POOL1, 4)]),
        ("Digestive enzymes", [(g_enz, 12), (uk_enz, 5), (POOL1, 2), (g_step, 1)]),
        ("Absorption and the small intestine", [(g_vil, 8), (g_step, 4), (POOL1, 2), (g_part, 4), (POOL5, 2)]),
        ("The liver", [(g_liv, 8), (g_enz, 6), (g_part, 3), (g_step, 2), (uk_enz, 1)]),
        ("Exam-style questions", [(POOL5, 9), (g_enz, 4), (g_vil, 3), (g_liv, 2), (uk_enz, 2)]),
    ])
    make_ol(LV, SUBJ, "nutrition-in-humans", SORT, "Nutrition in Humans",
            "Describe the functions of the main parts of the alimentary canal and associated organs in ingestion, digestion, absorption, assimilation and egestion; "
            "describe mechanical and chemical digestion, including the roles of amylase, maltase, proteases and lipase and of bile in emulsifying fats; describe "
            "the structure of a villus and how it is adapted for absorption; describe the hepatic portal vein and the roles of the liver in carbohydrate metabolism, "
            "deamination and the breakdown of alcohol (summary of the Singapore-Cambridge O-Level Biology 6093 syllabus).",
            "Nutrition in Humans", "Nutrition in humans",
            "Free Secondary 3 O-Level Biology worksheets on nutrition in humans: the alimentary canal, digestive enzymes, bile, villi and absorption, and the liver. "
            "100 questions with answers.",
            "Big insoluble molecules → small soluble ones.", "Absorbed in the ileum, sent to the liver by the hepatic portal vein.",
            "<p><b>Food passes mouth → oesophagus → stomach → duodenum → ileum → colon → rectum.</b></p><ul>"
            "<li>Starch → maltose (amylase) → glucose (maltase). Protein → polypeptides (pepsin, trypsin) → amino acids (peptidase). Fat → fatty acids + glycerol (lipase).</li>"
            "<li>Bile, made in the liver and stored in the gall bladder, emulsifies fat. It is not an enzyme.</li>"
            "<li>Villi give a huge surface area, thin walls, capillaries and lacteals for absorption.</li>"
            "<li>The liver stores glycogen, deaminates excess amino acids to urea and breaks down alcohol.</li></ul>",
            [("Enzyme for maltose → glucose?", ["maltose is the substrate"], "maltase"),
             ("Why many villi?", ["villi increase surface area"], "faster absorption")],
            ["Calling bile an enzyme.", "Saying protein digestion starts in the mouth.", "Saying most absorption happens in the stomach or colon.",
             "Saying villi increase the volume rather than the surface area."],
            [("What is the difference between digestion and absorption?", "Digestion breaks large, insoluble food molecules into small, soluble ones. Absorption is the movement of these small molecules through the wall of the small intestine into the blood or lymph."),
             ("How is a villus adapted for absorption?", "It has microvilli for a large surface area, a wall one cell thick, a rich supply of capillaries to keep a steep gradient and a lacteal to absorb fats."),
             ("What does the liver do with excess amino acids?", "It deaminates them: the amino group is removed and converted to urea, which is excreted by the kidneys; the rest can be used for energy.")],
            sets)


if __name__ == "__main__":
    main()
