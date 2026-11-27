# -*- coding: utf-8 -*-
"""
Australian food webs for the AU science units (bushland, billabong, Great Barrier Reef, outback).
add() puts them into sci_foodweb at run time only, so the US and SG units that pick from sci_foodweb.WEBS do not change.
Diets are simplified but true: koalas eat eucalyptus leaves, platypus eat yabbies and insect larvae, thorny devils eat ants,
powerful owls hunt possums, dingoes hunt kangaroos.
"""
import sci_foodweb as FW

AUW = {
    "bush": {"name": "bushland habitat", "producers": ["gum tree", "grass"],
             "eats": {"koala": ["gum tree"], "possum": ["gum tree"], "kangaroo": ["grass"], "grasshopper": ["grass"], "mouse": ["grass"],
                      "kookaburra": ["grasshopper", "mouse"], "brown snake": ["mouse"], "powerful owl": ["possum"], "dingo": ["kangaroo"]}},
    "billabong": {"name": "billabong", "producers": ["algae", "waterweed"],
                  "eats": {"tadpole": ["algae"], "mosquito larva": ["algae"], "yabby": ["waterweed"], "snail": ["waterweed", "algae"],
                           "dragonfly nymph": ["mosquito larva", "tadpole"], "platypus": ["yabby", "dragonfly nymph"],
                           "Murray cod": ["yabby"], "heron": ["tadpole", "yabby"]}},
    "reef": {"name": "coral reef", "producers": ["phytoplankton", "seaweed"],
             "eats": {"zooplankton": ["phytoplankton"], "parrotfish": ["seaweed"], "green turtle": ["seaweed"], "small fish": ["zooplankton"],
                      "coral trout": ["small fish"], "reef shark": ["coral trout", "parrotfish"]}},
    "outback": {"name": "outback desert", "producers": ["native grass", "saltbush"],
                "eats": {"ant": ["native grass"], "grasshopper": ["native grass"], "hopping mouse": ["native grass"], "red kangaroo": ["native grass", "saltbush"],
                         "thorny devil": ["ant"], "bearded dragon": ["grasshopper"], "goanna": ["hopping mouse", "bearded dragon"],
                         "dingo": ["red kangaroo", "hopping mouse"]}},
}
LAY = {
    "bush": {"gum tree": (.22, 0), "grass": (.72, 0), "koala": (.04, 1), "possum": (.24, 1), "kangaroo": (.45, 1), "grasshopper": (.7, 1), "mouse": (.94, 1),
             "powerful owl": (.2, 2), "dingo": (.45, 2), "kookaburra": (.7, 2), "brown snake": (.86, 3)},
    "billabong": {"algae": (.28, 0), "waterweed": (.75, 0), "tadpole": (.08, 1), "mosquito larva": (.36, 1), "snail": (.62, 1), "yabby": (.88, 1),
                  "dragonfly nymph": (.25, 2), "Murray cod": (.88, 2), "heron": (.62, 3), "platypus": (.3, 3)},
    "reef": {"phytoplankton": (.22, 0), "seaweed": (.75, 0), "zooplankton": (.18, 1), "parrotfish": (.6, 1), "green turtle": (.86, 1),
             "small fish": (.2, 2), "coral trout": (.3, 3), "reef shark": (.62, 4)},
    "outback": {"native grass": (.3, 0), "saltbush": (.78, 0), "ant": (.04, 1), "grasshopper": (.25, 1), "hopping mouse": (.54, 1), "red kangaroo": (.85, 1),
                "thorny devil": (.13, 2), "bearded dragon": (.62, 2), "goanna": (.3, 3), "dingo": (.93, 2)},
}
PLANTS = {"gum tree", "grass", "algae", "waterweed", "phytoplankton", "seaweed", "native grass", "saltbush"}
MASS = {"grass", "algae", "waterweed", "phytoplankton", "seaweed", "native grass", "saltbush", "zooplankton"}
PLUR = {"gum tree": "gum trees", "mosquito larva": "mosquito larvae", "dragonfly nymph": "dragonfly nymphs", "small fish": "small fish",
        "parrotfish": "parrotfish", "coral trout": "coral trout", "Murray cod": "Murray cod", "yabby": "yabbies", "possum": "possums",
        "powerful owl": "powerful owls", "brown snake": "brown snakes", "green turtle": "green turtles", "reef shark": "reef sharks",
        "hopping mouse": "hopping mice", "mouse": "mice", "red kangaroo": "red kangaroos", "thorny devil": "thorny devils",
        "bearded dragon": "bearded dragons", "goanna": "goannas", "dingo": "dingoes", "zooplankton": "zooplankton", "platypus": "platypuses",
        "tadpole": "tadpoles", "snail": "snails", "koala": "koalas", "kangaroo": "kangaroos", "grasshopper": "grasshoppers", "kookaburra": "kookaburras",
        "heron": "herons", "ant": "ants"}


def add():
    FW.WEBS.update(AUW)
    FW.LAYOUT.update(LAY)
    FW.PLANTS |= PLANTS
    for m in MASS:
        FW.ART[m] = ""
    FW.PLURAL.update(PLUR)
    for m in MASS:
        FW.PLURAL.setdefault(m, m)


NAMES = sorted(AUW)
