# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Comparing Length, Capacity and Weight (TEKS K.7A, K.7B)
  python3 tools/gen_ustx_math_gk_comparing_measures.py
Longer or shorter, taller or shorter, heavier or lighter, holds more or less (US Kindergarten makers with Texas
names; capacity from the Australian Foundation maker), and comparing stories.
Wrong answers come from real mistakes: not lining up the ends, thinking bigger is always heavier, and mixing up more
and less.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_compare_length_and_weight as cl
adopt(cl)
import gen_au_maths_f_comparing_length_mass_capacity as cc
adopt(cc)
tx_common.GRADE = "kindergarten"



def build():
    sets, R = build_sets([
        ("Longer or shorter", [("run", cl.set_two, ("rnd", cl.Kids), 20)]),
        ("Taller or shorter", [("run", cl.set_towers, ("rnd", cl.Kids), 20)]),
        ("Heavier or lighter", [("run", cl.set_balance, ("rnd", cl.Kids), 20)]),
        ("Holds more or less", [("run", cc.set_capacity, ("rnd",), 20)]),
        ("Comparing stories", [("run", cl.set_words, ("rnd", cl.Kids), 20)]),
    ], 69014)
    finish(sets, R)
    body = lesson('<ul><li><b>Length</b>: line up the ends. The one that sticks out is <b>longer</b>.</li><li><b>Weight</b>: on a balance, the <b>heavier</b> side goes down.</li><li><b>Capacity</b>: the container that holds more water has more capacity.</li><li>Say how they are different: “The pencil is longer than the crayon.”</li></ul>',
        [example("A pencil and a crayon, lined up", ["the pencil sticks out"], "the pencil is longer")],
        [['Not lining up the ends', 'Start both at the same place.'], ['Thinking bigger is always heavier', 'A big balloon is light.'], ['Mixing up more and less', 'Less means a smaller amount.']])
    faq = [('What does TEKS K.7A ask?', 'Give an example of a measurable attribute of a given object, including length, capacity, and weight.'), ('What does TEKS K.7B ask?', 'Compare two objects with a common measurable attribute to see which object has more of/less of the attribute and describe the difference.'), ('How does a balance work?', 'The heavier side goes down.'), ('What is capacity?', 'How much a container holds.')]
    make('comparing-length-capacity-and-weight', 14, 'Geometry and Measurement', 'K.7A, K.7B',
         'K.7A give an example of a measurable attribute of a given object, including length, capacity, and weight; K.7B compare two objects with a common measurable attribute to see which object has more of/less of the attribute and describe the difference',
         'Comparing Length, Capacity and Weight', 'Comparing Length, Capacity and Weight',
         'Free kindergarten measurement worksheets for Texas TEKS K.7A and K.7B: compare length, height, weight and capacity with pictures. 100 questions with answers.',
         'Line up the ends to compare length.', 'On a balance, the heavier side goes down.',
         body, faq, sets, seo_title='Kindergarten Comparing Length, Capacity and Weight Worksheets (TEKS K.7B)')


if __name__ == "__main__":
    build()
