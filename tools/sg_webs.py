# -*- coding: utf-8 -*-
"""
Singapore food webs for the Primary 6 environment units (mangrove, school garden, pond, sea).
add() puts them into sci_foodweb at run time only, so the US units that pick from sci_foodweb.WEBS do not change.
The diets are simplified but true (mudskippers eat algae and small snails; kingfishers catch mudskippers and crabs).
"""
import sci_foodweb as FW

SG = {
    "mangrove": {"name": "mangrove swamp", "producers": ["mangrove tree", "algae"],
                 "eats": {"snail": ["algae"], "crab": ["mangrove tree", "algae"], "mudskipper": ["algae", "snail"],
                          "kingfisher": ["mudskipper", "crab"], "monitor lizard": ["crab", "mudskipper"], "heron": ["mudskipper"]}},
    "garden": {"name": "school garden", "producers": ["hibiscus", "grass"],
               "eats": {"aphid": ["hibiscus"], "caterpillar": ["hibiscus"], "grasshopper": ["grass"], "ladybird": ["aphid"], "spider": ["grasshopper"],
                        "mynah": ["caterpillar", "grasshopper"], "garden lizard": ["spider", "grasshopper"], "snake": ["mynah", "garden lizard"]}},
    "sgpond": {"name": "pond", "producers": ["algae", "water lettuce"],
               "eats": {"snail": ["algae", "water lettuce"], "mosquito larva": ["algae"], "guppy": ["mosquito larva", "algae"], "dragonfly nymph": ["mosquito larva"],
                        "frog": ["dragonfly nymph", "snail"], "heron": ["frog", "guppy"], "turtle": ["snail", "water lettuce"]}},
    "sea": {"name": "coral reef", "producers": ["phytoplankton", "seaweed"],
            "eats": {"zooplankton": ["phytoplankton"], "parrotfish": ["seaweed"], "sea urchin": ["seaweed"], "small fish": ["zooplankton"],
                     "squid": ["small fish"], "shark": ["squid", "parrotfish"]}},
}
LAY = {
    "mangrove": {"mangrove tree": (.25, 0), "algae": (.75, 0), "crab": (.22, 1), "snail": (.8, 1), "mudskipper": (.58, 2),
                 "kingfisher": (.18, 3), "monitor lizard": (.55, 3), "heron": (.9, 3)},
    "garden": {"hibiscus": (.25, 0), "grass": (.75, 0), "aphid": (.08, 1), "caterpillar": (.36, 1), "grasshopper": (.78, 1), "ladybird": (.1, 2),
               "spider": (.92, 2), "mynah": (.38, 3), "garden lizard": (.76, 3), "snake": (.6, 4)},
    "sgpond": {"water lettuce": (.2, 0), "algae": (.66, 0), "snail": (.2, 1), "mosquito larva": (.65, 1), "turtle": (.08, 2), "guppy": (.5, 2),
               "dragonfly nymph": (.86, 2), "frog": (.42, 3), "heron": (.7, 4)},
    "sea": {"phytoplankton": (.2, 0), "seaweed": (.75, 0), "zooplankton": (.15, 1), "parrotfish": (.55, 1), "sea urchin": (.9, 1),
            "small fish": (.2, 2), "squid": (.3, 3), "shark": (.58, 4)},
}
PLANTS = {"mangrove tree", "algae", "hibiscus", "grass", "water lettuce", "phytoplankton", "seaweed"}
MASS = {"algae", "grass", "water lettuce", "phytoplankton", "seaweed", "zooplankton"}
PLUR = {"mangrove tree": "mangrove trees", "mosquito larva": "mosquito larvae", "dragonfly nymph": "dragonfly nymphs", "small fish": "small fish",
        "parrotfish": "parrotfish", "squid": "squid", "guppy": "guppies", "hibiscus": "hibiscus plants", "zooplankton": "zooplankton",
        "monitor lizard": "monitor lizards", "garden lizard": "garden lizards", "ladybird": "ladybirds", "sea urchin": "sea urchins", "mudskipper": "mudskippers"}


def add():
    FW.WEBS.update(SG)
    FW.LAYOUT.update(LAY)
    FW.PLANTS |= PLANTS
    for m in MASS:
        FW.ART[m] = ""
    FW.PLURAL.update(PLUR)
    for m in MASS:
        FW.PLURAL.setdefault(m, m)


NAMES = sorted(SG)
