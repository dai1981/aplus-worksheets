# -*- coding: utf-8 -*-
"""
US High School Physics: Digital and Analog Signals (HS-PS4-2)
  python tools/gen_us_science_phys_digital_and_analog_signals.py
Evaluate questions about the advantages of using a digital transmission and storage of information.
Analog vs digital signals, bits, bytes and binary numbers, how many values n bits can store (2ⁿ), sampling,
file sizes and download times (bits vs bytes), noise, copying, compression and the drawbacks of digital data.
Wrong answers come from real mistakes: "8 bits store 8 values", "megabytes and megabits are the same",
"digital copies lose quality", "digital signals have no drawbacks".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_phys import num, uniq, safe

U = Unit(90313)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


@safe
def g_bits():
    k = R.choice(["vals", "need"])
    if k == "vals":
        n = R.choice([1, 2, 3, 4, 5, 6, 8, 10, 12, 16])
        if not once(("bv", n)):
            return None
        v = 2 ** n
        g = num(v)
        return item("How many different values can %d bits represent?" % n, g, uniq(g, [num(n), num(2 * n), num(n * n), num(v - 1), num(v * 2)]), "2<sup>%d</sup> = %s." % (n, num(v)))
    N = R.choice([3, 5, 10, 20, 26, 30, 50, 60, 100, 200, 256, 500, 1000])
    if not once(("bn", N)):
        return None
    n = 0
    while 2 ** n < N:
        n += 1
    g = "%d bits" % n
    return item("What is the smallest number of bits needed to give each of %s items its own code?" % num(N), g, uniq(g, ["%d bits" % (n - 1), "%d bits" % (n + 1), "%s bits" % num(N), "%d bits" % (N // 2)]),
                "2<sup>%d</sup> = %s is enough, but 2<sup>%d</sup> = %s is not." % (n, num(2 ** n), n - 1, num(2 ** (n - 1))))


@safe
def g_binary():
    k = R.choice(["d", "b"])
    n = R.randint(2, 63)
    if not once(("bi", n, k)):
        return None
    b = bin(n)[2:]
    if k == "d":
        g = str(n)
        return item("What decimal number is the binary number %s?" % b, g, uniq(g, [str(int(b[::-1], 2)), str(len(b)), str(b.count("1")), str(n + 1), str(n * 2)]),
                    "Add the place values (1, 2, 4, 8, 16, 32) that have a 1.")
    g = b
    w = [bin(n + 1)[2:], bin(n - 1)[2:], b[::-1], "1" + b]
    return item("What is %d written in binary?" % n, g, uniq(g, w), "%d = %s." % (n, " + ".join(str(2 ** i) for i in reversed(range(len(b))) if b[len(b) - 1 - i] == "1")))


@safe
def g_dl():
    who = P.next()[0]
    MB = R.choice([10, 25, 50, 100, 200, 400, 500, 1000])
    sp = R.choice([5, 10, 20, 25, 40, 50, 100, 200])
    t = MB * 8 / sp
    if t != round(t, 1) or not once(("dl", MB, sp)):
        return None
    g = "%s s" % num(t, 1)
    return item("%s downloads a %s MB (megabyte) file on a %d Mbps (megabits per second) connection. About how long does it take? (1 byte = 8 bits)" % (who, num(MB), sp), g,
                uniq(g, ["%s s" % num(MB / sp, 2), "%s s" % num(MB * sp), "%s s" % num(t * 8, 1), "%s s" % num(sp / MB, 3)]), "%s MB × 8 = %s Mb; %s ÷ %d = %s s." % (num(MB), num(MB * 8), num(MB * 8), sp, num(t, 1)))


@safe
def g_size():
    k = R.choice(["img", "audio"])
    if k == "img":
        w, h = R.choice([(100, 100), (200, 100), (640, 480), (800, 600), (1000, 1000), (320, 240)])
        b = R.choice([1, 8, 24])
        if not once(("im", w, h, b)):
            return None
        bits = w * h * b
        g = "%s bytes" % num(bits / 8)
        return item("A %s × %s pixel image uses %d bit%s per pixel. How many bytes is it (no compression)?" % (num(w), num(h), b, "" if b == 1 else "s"), g,
                    uniq(g, ["%s bytes" % num(bits), "%s bytes" % num(w * h), "%s bytes" % num(bits / 64), "%s bytes" % num(w * h * b * 8)]), "%s pixels × %d bits = %s bits ÷ 8 = %s bytes." % (num(w * h), b, num(bits), num(bits / 8)))
    rate = R.choice([8000, 16000, 22050, 44100])
    bits = R.choice([8, 16])
    s = R.choice([1, 2, 5, 10, 60])
    if not once(("au", rate, bits, s)):
        return None
    tot = rate * bits * s
    g = "%s bits" % num(tot)
    return item("A mono recording takes %s samples per second with %d bits per sample. How many bits are in %d s of sound?" % (num(rate), bits, s), g,
                uniq(g, ["%s bits" % num(rate * s), "%s bits" % num(rate * bits), "%s bits" % num(tot / 8), "%s bits" % num(tot * 2)]), "%s × %d × %d = %s bits." % (num(rate), bits, s, num(tot)))


ADV = [("A digital phone call stays clear even though the signal picks up some noise.", "Receivers only need to tell 0 from 1, so small noise is ignored."),
       ("A song file is copied 100 times and the last copy sounds exactly like the first.", "Digital copies are exact copies of the bits."),
       ("A whole movie fits on a small memory card.", "Digital data can be compressed and stored densely."),
       ("Banking apps scramble data before sending it.", "Digital data can be encrypted for security."),
       ("A space probe's pictures arrive correctly from billions of kilometers away.", "Error-checking codes can find and fix wrong bits."),
       ("A photo can be sent to thousands of people in seconds.", "Digital files are easy to transmit and share.")]
DIS = [("A digital recording misses some tiny details of the original sound wave.", "Sampling records only separate points, not the whole smooth wave."),
       ("Old files on a floppy disk can no longer be opened.", "Digital formats and hardware can become outdated."),
       ("Personal data is stolen from a company's server.", "Stored digital data can be hacked or leaked."),
       ("A video call freezes when the network is weak.", "If too many bits are lost, the signal can fail completely.")]


@safe
def g_adv():
    if R.random() < 0.6:
        s, a = R.choice(ADV)
        pool = [x[1] for x in ADV if x[1] != a] + [x[1] for x in DIS]
        if not once(("ad", s)):
            return None
        return item("%s Which advantage of digital information does this show?" % s, a, R.sample(pool, 3), "Digital signals resist noise and copy perfectly.")
    s, a = R.choice(DIS)
    if not once(("ds", s)):
        return None
    return item("%s Which drawback of digital information does this show?" % s, a, R.sample([x[1] for x in DIS if x[1] != a] + [x[1] for x in ADV], 3), "Digital has trade-offs.")


AD = [("a vinyl record's groove", "analog"), ("a mercury thermometer", "analog"), ("an MP3 file", "digital"), ("a text message", "digital"), ("a clock with hands", "analog"),
      ("a QR code", "digital"), ("an AM radio broadcast", "analog"), ("a photo on a phone", "digital"), ("a film camera negative", "analog"), ("a streaming video", "digital"),
      ("the sound wave from a voice", "analog"), ("a barcode", "digital")]


@safe
def g_ad():
    s, k = R.choice(AD)
    if not once(("ag", s)):
        return None
    return item("Is %s analog or digital?" % s, k, ["digital" if k == "analog" else "analog", "neither; it has no information", "both at the same time"],
                "Analog varies smoothly; digital uses separate values (bits).")


B1 = bank([
    ("What is an analog signal?", "a signal that changes smoothly and continuously", ["a signal made only of 0s and 1s", "a signal with no information", "a signal that cannot be stored"], "Like a sound wave."),
    ("What is a digital signal?", "a signal made of separate values, usually 0s and 1s", ["a signal that changes smoothly", "a signal with no noise ever", "a signal that only travels by wire"], "Bits."),
    ("What is a bit?", "a single binary digit, 0 or 1", ["8 binary digits", "a type of wave", "one second of sound"], "Binary digit."),
    ("How many bits are in a byte?", "8", ["2", "4", "10"], "1 byte = 8 bits."),
    ("Why are digital signals less affected by noise?", "A receiver only has to decide between 0 and 1.", ["Digital signals are louder.", "Noise cannot exist.", "They travel faster than light."], "Thresholds."),
    ("What does sampling do in a digital recording?", "measures the analog signal at regular time intervals", ["makes the sound louder", "removes all noise", "turns bits into light"], "Sample rate."),
    ("Why does a higher sampling rate give a better recording?", "It captures more points of the original wave.", ["It makes the file smaller.", "It removes bits.", "It changes the pitch."], "More detail."),
    ("What is compression?", "a way to make a file smaller by removing or encoding repeated data", ["making a file larger", "copying a file", "changing analog to light"], "ZIP, MP3, JPEG."),
])
B5 = bank([
    ("Why did most TV and radio switch from analog to digital?", "Digital sends more channels with clearer pictures and sound in the same bandwidth.", ["Digital is always free.", "Analog cannot carry sound.", "Digital needs no transmitters."], "Efficiency."),
    ("A music fan says vinyl sounds 'warmer' than digital. Which is a fair way to test this claim?", "a blind listening test comparing the same song on both", ["ask the fan again", "measure the record's weight", "look at the cover art"], "Evaluate claims."),
    ("Why do hospitals back up digital medical records in several places?", "Digital data can be lost if one device fails, but copies are exact.", ["Paper is better.", "Digital data never fails.", "Copies lose quality."], "Redundancy."),
    ("A student says digital information is always better. What is a balanced reply?", "It has big advantages but also risks like hacking, outdated formats and sampling loss.", ["The student is completely right.", "Digital is always worse.", "There is no difference."], "Trade-offs."),
    ("Why does a 16-bit audio file sound better than an 8-bit one?", "16 bits give 65,536 levels instead of 256, so the wave is copied more closely.", ["16-bit files are louder.", "8-bit files have no sound.", "The bits are larger."], "Resolution."),
])


def body():
    think = ("<p><b>Digital information is stored and sent as bits (0s and 1s).</b></p>"
             "<ul><li>n bits can show 2<sup>n</sup> different values. 1 byte = 8 bits.</li>"
             "<li>Advantages: resists noise, copies perfectly, can be compressed, encrypted and error-checked.</li>"
             "<li>Drawbacks: sampling misses some detail, data can be hacked or lost, and formats go out of date.</li></ul>")
    ex = [("How many values with 4 bits?", ["2<sup>4</sup>"], "16"),
          ("100 MB file at 50 Mbps?", ["100 × 8 = 800 Mb", "800 ÷ 50"], "16 s")]
    mist = ["Thinking 8 bits store only 8 values.", "Mixing up megabytes (MB) and megabits (Mb).", "Thinking digital has no drawbacks."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Analog and digital", B1 + [(g_ad, 8), (g_bits, 4)]),
        ("Bits and binary", [(g_bits, 10), (g_binary, 10)]),
        ("File sizes and downloads", [(g_size, 10), (g_dl, 10)]),
        ("Advantages and drawbacks", [(g_adv, 8), (g_binary, 8), (g_bits, 4)]),
        ("Evaluating digital technology", B5 + [(g_dl, 6), (g_size, 5), (g_ad, 2), (g_binary, 2)]),
    ])
    make("physics", "digital-and-analog-signals", 13, "HS-PS4-2",
         "Evaluate questions about the advantages of using a digital transmission and storage of information.",
         "Digital and Analog Signals",
         "Digital Signals Worksheets: Bits, Binary, File Sizes and Analog vs Digital (Physics)",
         "Digital Signals",
         "Free high school physics worksheets on digital and analog signals (NGSS HS-PS4-2): bits and binary, 2ⁿ values, file sizes, download times and the advantages and drawbacks of digital data. 100 questions with answers.",
         "Digital = bits, 0s and 1s.",
         "Digital resists noise and copies perfectly, but sampling, hacking and old formats are risks.",
         body(),
         [("What is the difference between analog and digital signals?", "An analog signal changes smoothly. A digital signal uses separate values, usually bits (0 and 1)."),
          ("How many values can n bits store?", "2ⁿ values. For example, 8 bits (1 byte) can store 256 different values."),
          ("What are the advantages of digital signals?", "They resist noise, can be copied perfectly, compressed, encrypted and checked for errors.")],
         sets)


if __name__ == "__main__":
    main()
