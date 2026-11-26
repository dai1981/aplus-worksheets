# -*- coding: utf-8 -*-
"""
Pictures and helpers for UK KS1 science (Year 1 and Year 2): sci_kids icons with British names (ladybird, not ladybug),
a picture card, a row of pictures with words, and a simple "which of these" maker.
"""
from sci_common import fig, item
import sci_kids as K

UKNAME = {"bug": "ladybird", "flashlight": "torch", "glass": "glass window"}


def name(kind):
    return UKNAME.get(kind, K.name(kind))


def card(kind, size=110):
    return fig(K.card(kind, size, "a picture of a %s" % name(kind)))


def row(kinds, words=None, size=90):
    words = words or [name(k) for k in kinds]
    return fig(K.row(kinds, words=words, size=size, label="pictures: " + ", ".join(words)))


def which_of(R, once, key, q, yes, no, e, n=1):
    """'Which of these is ...: a, b, c or d?' with one answer from yes and three from no."""
    a = R.choice(yes)
    if not once((key, a), n):
        return None
    w = R.sample(no, 3)
    o = sorted([a] + w)
    return item("%s: %s or %s?" % (q, ", ".join(o[:3]), o[3]), a, w, e)
