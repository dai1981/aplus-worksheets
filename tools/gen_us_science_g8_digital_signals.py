# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Digital Signals (MS-PS4-3)
  python tools/gen_us_science_g8_digital_signals.py
Integrate qualitative scientific and technical information to support the claim that digitized signals are a more
reliable way to encode and transmit information than analog signals. Analog vs. digital, bits and binary
(n bits → 2^n patterns), noise and copying, sampling, wired / wireless / fiber transmission.
Wrong answers come from real mistakes: "digital means electronic", "analog signals are copied perfectly",
"3 bits make 6 patterns", "noise does not affect analog signals".
"""
from sci_common import Unit, item, bank, lesson, make, table, People, comma

U = Unit(80110)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


EX = {"analog": ["a vinyl record", "a cassette tape", "a film camera photo", "an old AM radio broadcast", "a mercury thermometer", "a clock with hands", "a landline phone call from the 1970s"],
      "digital": ["an MP3 song file", "a photo from a phone camera", "a text message", "a streamed video", "a digital thermometer reading", "a QR code", "a file on a USB drive"]}


def g_kind():
    k = R.choice(sorted(EX))
    x = R.choice(EX[k])
    who = P.next()[0]
    if not once(("k", x)):
        return None
    other = "digital" if k == "analog" else "analog"
    return item("%s looks at %s. Does it store information as an analog or a digital signal?" % (who, x), k, [other, "neither, it has no information", "both at once"],
                "Analog signals vary smoothly; digital signals use a set of separate values (usually 0s and 1s).")


def g_bits():
    n = R.choice([1, 2, 3, 4, 5, 6, 7, 8, 10])
    who = P.next()[0]
    k = R.choice(["patterns", "need"])
    if not once((k, n)):
        return None
    if k == "patterns":
        return item("%s's code uses %d bit%s. How many different patterns of 0s and 1s can it make?" % (who, n, "" if n == 1 else "s"), comma(2 ** n),
                    [comma(2 * n), comma(n * n) if n * n != 2 ** n else comma(2 ** n + 2), comma(2 ** (n - 1)) if n > 1 else "3"], "Each bit doubles the patterns: 2^%d = %s." % (n, comma(2 ** n)))
    m = 2 ** n
    c = R.randint(2 ** (n - 1) + 1, m) if n > 1 else 2
    return item("%s needs a different code for each of %s colors. What is the fewest number of bits needed?" % (who, comma(c)), "%d bit%s" % (n, "" if n == 1 else "s"),
                ["%d bits" % (n + 1), "%d bit%s" % (n - 1, "" if n - 1 == 1 else "s") if n > 1 else "3 bits", "%s bits" % comma(c)],
                "%d bits give %s patterns, which is enough; %d bits give only %s." % (n, comma(m), n - 1, comma(m // 2)) if n > 1 else "1 bit gives 2 patterns.")


def g_bin():
    v = R.randint(1, 31)
    b = format(v, "b").zfill(5)
    who = P.next()[0]
    k = R.choice(["to", "from"])
    if not once((k, v)):
        return None
    if k == "to":
        w = {format(x, "b").zfill(5) for x in [v + 1, v - 1, v ^ 16, v ^ 1, v ^ 2] if 0 < x < 32 and x != v}
        if len(w) < 3:
            return None
        return item("%s writes a number as 5 bits using place values 16, 8, 4, 2, 1. How is %d written?" % (who, v), b, R.sample(sorted(w), 3), "Add the place values with a 1: %d." % v)
    w = {str(x) for x in [v + 1, v - 1, int(b[::-1], 2), v + 16 if v < 16 else v - 16, b.count("1")] if x != v and x > 0}
    if len(w) < 3:
        return None
    return item("%s receives the 5-bit code %s (place values 16, 8, 4, 2, 1). What number is it?" % (who, b), str(v), R.sample(sorted(w), 3),
                " + ".join(str(16 >> i) for i, ch in enumerate(b) if ch == "1") + " = %d." % v)


NOISE = [("A song is copied from tape to tape ten times.", "The sound gets worse with each copy because noise adds up.", "Each copy is a perfect match."),
         ("A digital photo is copied ten times.", "Each copy is identical, because the same 0s and 1s are copied.", "The photo gets blurrier with each copy."),
         ("A radio station's analog signal passes through a storm.", "Static noise is added and cannot easily be removed.", "The storm makes the sound clearer."),
         ("A digital TV signal gets a little noise.", "The receiver can still tell 0s from 1s, so the picture stays clear.", "The picture gets slightly fuzzy, like an old TV."),
         ("A digital signal travels through a long fiber-optic cable.", "Repeaters can rebuild clean 0s and 1s along the way.", "The signal must get noisier at every repeater."),
         ("An error-checking code is added to a digital message.", "The receiver can detect and fix some errors.", "The message becomes analog.")]


def g_noise():
    s, a, w0 = R.choice(NOISE)
    who = P.next()[0]
    if not once(("n", s)):
        return None
    return item("%s reads: “%s” What is most likely to happen?" % (who, s), a, [w0, "The information is lost completely and cannot be sent.", "The signal turns into a sound wave in space."],
                "Digital signals resist noise and copy perfectly; analog signals pick up noise.")


def g_size():
    who = P.next()[0]
    k = R.choice(["bytes", "time"])
    if k == "bytes":
        b = R.choice([2, 3, 4, 5, 6, 8, 10, 12])
        if not once(("b", b)):
            return None
        return item("A byte is 8 bits. %s's message is %d bytes long. How many bits is that?" % (who, b), "%d bits" % (8 * b), ["%d bits" % (b + 8), "%d bits" % b, "%d bits" % (16 * b)], "%d × 8 = %d bits." % (b, 8 * b))
    mb = R.choice([10, 20, 40, 50, 100, 200])
    sp = R.choice([5, 10, 20, 25])
    if mb % sp or mb == sp or not once(("t", mb, sp)):
        return None
    return item("%s downloads a %d MB file at %d MB per second. How long does it take?" % (who, mb, sp), "%d seconds" % (mb // sp), ["%d seconds" % (mb * sp), "%d seconds" % (mb - sp) if mb - sp != mb // sp + 2 else "%d seconds" % (mb + sp), "%d seconds" % (mb // sp + 2)],
                "%d ÷ %d = %d s." % (mb, sp, mb // sp))


B1 = bank([
    ("What is an analog signal?", "a signal that changes smoothly and continuously, like a wave", ["a signal made only of 0s and 1s", "a signal that never changes", "a computer file"], "Records and old radios are analog."),
    ("What is a digital signal?", "a signal made of separate values, usually 0s and 1s", ["any signal from electricity", "a smooth wave", "a signal from a wire only"], "Digital means discrete steps."),
    ("What is a bit?", "a single 0 or 1", ["8 bytes", "a color", "a sound wave"], "Short for binary digit."),
    ("Why are digital signals more reliable than analog signals?", "Small amounts of noise do not change whether a value is read as 0 or 1.", ["They use more electricity.", "They never travel through wires.", "They are always louder."],
     "Noise is easier to ignore."),
    ("Why can digital files be copied many times without losing quality?", "Each copy has exactly the same 0s and 1s.", ["Copies get better each time.", "Digital files cannot be copied.", "Each copy is smoothed out."], "Perfect copies."),
    ("How is a sound turned into a digital signal?", "It is measured (sampled) many times per second and each measurement is stored as a number.", ["It is painted on paper.", "It is made louder.", "It is stored as a smooth groove."],
     "More samples give a better copy."),
    ("Which is a way to send digital signals?", "fiber-optic cables using pulses of light", ["shouting louder", "carrier pigeons with records", "only vinyl records"], "Light pulses carry bits."),
    ("How many bits are in one byte?", "8", ["2", "10", "16"], "1 byte = 8 bits."),
])
B5 = bank([
    ("Ava claims digital music is more reliable than cassette tapes. Which evidence supports her?", "Digital copies sound the same after many copies; tapes get more hiss each time.", ["Tapes are bigger.", "Digital music is newer.", "Tapes cost more."],
     "Evidence about quality over copies."),
    ("Leo samples a sound 2 times per second instead of 40,000 times. What happens?", "The digital copy will be a very poor match to the real sound.", ["It sounds better.", "Nothing changes.", "The file becomes analog."], "More samples, better detail."),
    ("Mia's video call freezes in blocks but the sound stays clear. What kind of signal is it?", "digital", ["analog", "magnetic only", "not a signal"], "Digital errors show as blocks or dropouts, not fuzz."),
    ("Why do space probes send data back to Earth digitally?", "Weak signals over huge distances are easier to read and correct as 0s and 1s.", ["Space blocks analog signals completely.", "Digital is louder in space.", "Probes cannot make analog signals."],
     "Reliability over long distances."),
    ("One disadvantage of digital signals is that:", "they need equipment to convert them back to sound or pictures", ["they cannot be copied", "they always have static", "they cannot be stored"], "Digital needs encoding and decoding."),
])


def body():
    think = ("<p>Information can be sent as an <b>analog signal</b> (a smooth, continuous wave, like a vinyl record) or a <b>digital signal</b> (separate values, usually <b>0s and 1s</b>).</p>"
             "<ul><li>A <b>bit</b> is one 0 or 1. <b>n bits make 2<sup>n</sup> patterns</b> (3 bits → 8 patterns). 8 bits = 1 byte.</li>"
             "<li>To digitize a sound or picture, it is <b>sampled</b> and each sample is stored as a number.</li>"
             "<li>Digital signals are <b>more reliable</b>: noise does not easily change a 0 into a 1, signals can be rebuilt and checked for errors, and copies are perfect.</li></ul>")
    ex = [("How many patterns can 4 bits make?", ["2 × 2 × 2 × 2"], "16"),
          ("Why does a copied tape get worse?", ["Analog noise adds up."], "Each copy adds noise.")]
    mist = ["Thinking digital just means electronic. It means separate values.",
            "Thinking n bits make 2 × n patterns. They make 2ⁿ.",
            "Thinking analog copies are perfect."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Analog and digital", B1 + [(g_kind, 12)]),
        ("Bits and patterns", [(g_bits, 12), (g_size, 8)]),
        ("Binary codes", [(g_bin, 14), (g_bits, 6)]),
        ("Noise and reliability", [(g_noise, 6), (g_kind, 2), (g_bin, 6), (g_size, 6)]),
        ("Supporting the claim", B5 + [g_noise, g_bits, g_bin, g_size]),
    ])
    make("grade-8", "digital-signals", 10, "MS-PS4-3",
         "Integrate qualitative scientific and technical information to support the claim that digitized signals are a more reliable way to encode and transmit information than analog signals.",
         "Digital Signals",
         "Grade 8 Digital Signals Worksheets: Analog vs. Digital, Bits, Binary and Noise",
         "Digital Signals",
         "Free middle school science worksheets on digital signals (NGSS MS-PS4-3): analog vs. digital signals, bits and binary codes, sampling, noise and why digital signals are more reliable. 100 practice questions with answers.",
         "Digital signals resist noise and copy perfectly.",
         "Digital signals use 0s and 1s, so small noise does not change the message. n bits make 2ⁿ patterns.",
         body(),
         [("What is the difference between analog and digital signals?", "Analog signals change smoothly and continuously. Digital signals use separate values, usually 0s and 1s."),
          ("Why are digital signals more reliable?", "Noise rarely changes a 0 into a 1, signals can be rebuilt and checked for errors, and digital copies are exactly the same as the original."),
          ("How many patterns can bits make?", "Each extra bit doubles the number of patterns. n bits can make 2ⁿ patterns, so 8 bits make 256.")],
         sets)


if __name__ == "__main__":
    main()
