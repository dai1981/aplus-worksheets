# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 6, AC9S6U02: Earth's rotation causes day and night; its tilt and revolution around
the Sun cause the seasons and changing day length (southern hemisphere: summer is December to February).
  python tools/gen_au_science_y6_day_night_and_seasons.py
Own questions on Australian seasons, day length in Hobart, Sydney and Darwin, the Sun's height and shadows through the year,
plus the UK Year 5 day-and-night makers and the US Grade 5 sun-direction makers with Australian names.
Wrong answers come from real mistakes: thinking seasons happen because Earth is closer to the Sun in summer, thinking
the Sun moves around the Earth, and using northern-hemisphere months for the seasons.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 6, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

DN = "gen_uk_science_y5_day_night_and_the_moon"
uk_turn = limit(src(DN, "g_turn"), 3)
uk_sky = src(DN, "g_sky")
us_dir = limit(src("gen_us_science_g5_shadows_day_and_night", "g_dir", drop=["north", "south", "noon", "12 p", "tetherball", "mailbox"]), 4)
us_b1 = src.B("gen_us_science_g5_shadows_day_and_night", "B1", drop=["north", "south", "noon", "December", "June", "July", "winter", "summer", "United States", "spin around once", "causes day and night"])

US5 = "gen_us_science_g5_shadows_day_and_night"
us_graph = limit(src(US5, "g_shadow_graph"), 4)

RR = [("The Sun rises and sets each day.", "rotation"), ("Day changes to night.", "rotation"),
      ("Stars seem to move across the night sky.", "rotation"), ("Shadows change direction during the day.", "rotation"),
      ("The seasons change through the year.", "revolution"),
      ("A year passes.", "revolution"), ("Different star patterns are seen in winter and summer nights.", "revolution"),
      ("Day length slowly changes from summer to winter.", "revolution")]


def g_rr():
    st, k = R.choice(RR)
    return tq("%s Which movement of Earth mainly causes this?" % st, "Earth's %s (%s)" % (k, "spinning on its axis" if k == "rotation" else "orbiting the Sun"),
              ["Earth's %s (%s)" % (o, "spinning on its axis" if o == "rotation" else "orbiting the Sun") for o in ["rotation", "revolution"] if o != k] +
              ["the Moon orbiting Earth", "the Sun orbiting Earth"], "Rotation takes a day; revolution takes a year.")


SP = [("in the early morning", "low in the east", "long, pointing west"), ("in the mid-morning", "higher, in the north-east", "shorter, pointing south-west"),
      ("at midday", "highest, in the north", "shortest, pointing south"), ("in the mid-afternoon", "lower, in the north-west", "shorter, pointing south-east"),
      ("in the late afternoon", "low in the west", "long, pointing east")]


def g_sp():
    t, pos, sh = R.choice(SP)
    if R.random() < 0.5:
        w = sorted({x[1] for x in SP if x[1] != pos})
        return tq("In Sydney on a sunny day, where is the Sun %s?" % t, pos, R.sample(w, 3), "The Sun rises in the east, is highest in the north at midday and sets in the west.")
    w = sorted({x[2] for x in SP if x[2] != sh})
    return tq("In Sydney, what is a flagpole's shadow like %s?" % t, sh, R.sample(w, 3), "Shadows point away from the Sun.")


OPP = {"summer": "winter", "winter": "summer", "autumn": "spring", "spring": "autumn"}


def g_opp():
    se = R.choice(list(OPP))
    c = R.choice(["Melbourne", "Perth", "Adelaide", "Brisbane"])
    pl = R.choice(["Japan", "Canada", "Europe", "China"])
    from au_sci import once
    if not once(("opp", se, pl)):
        return None
    return tq("When it is %s in %s, which season is it in %s, in the northern hemisphere?" % (se, c, pl), OPP[se],
              [x for x in OPP if x != OPP[se]], "The two hemispheres have opposite seasons because of Earth's tilt.")


MONTHS = [("December", "summer"), ("January", "summer"), ("February", "summer"), ("March", "autumn"), ("April", "autumn"), ("May", "autumn"),
          ("June", "winter"), ("July", "winter"), ("August", "winter"), ("September", "spring"), ("October", "spring"), ("November", "spring")]


def g_month():
    m, se = R.choice(MONTHS)
    return tq("In southern Australia, which season is %s in?" % m, se, [x for x in ["summer", "autumn", "winter", "spring"] if x != se],
              "Australia is in the southern hemisphere: summer is December to February, winter is June to August.")


DL = [("Hobart", "June", "about 9 hours"), ("Hobart", "December", "about 15 hours"), ("Sydney", "June", "about 10 hours"),
      ("Sydney", "December", "about 14 and a half hours"), ("Darwin", "June", "about 11 and a half hours"), ("Darwin", "December", "about 12 and a half hours")]


def g_dl():
    c, m, h = R.choice(DL)
    w = sorted({x[2] for x in DL if x[2] != h})
    return tq("About how many hours of daylight does %s get on a clear day in late %s?" % (c, m), h, R.sample(w, 3),
              "Places further from the equator, such as Hobart, have the biggest change in day length between summer and winter.")


TAB2 = [("Hobart", "15 h 20 min", "9 h 00 min"), ("Sydney", "14 h 25 min", "9 h 55 min"), ("Brisbane", "13 h 50 min", "10 h 25 min"), ("Darwin", "12 h 50 min", "11 h 25 min")]


def g_tab2():
    tab = "<table class='sn-table'><tr><th>City</th><th>Day length, 21 December</th><th>Day length, 21 June</th></tr>%s</table>" % "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in TAB2)
    k = R.choice(["most", "least", "longest", "shortest", "pattern"])
    from au_sci import once
    if not once(("tab2", k)):
        return None
    if k == "most":
        return tq("%sWhich city's day length changes the most between December and June?" % tab, "Hobart", ["Darwin", "Brisbane", "Sydney"], "Hobart: about 6 hours 20 minutes of change.")
    if k == "least":
        return tq("%sWhich city's day length changes the least between December and June?" % tab, "Darwin", ["Hobart", "Sydney", "Brisbane"], "Darwin is closest to the equator.")
    if k == "longest":
        return tq("%sWhich city has the longest day on 21 December?" % tab, "Hobart", ["Darwin", "Brisbane", "Sydney"], "Hobart is furthest south.")
    if k == "shortest":
        return tq("%sWhich city has the shortest day on 21 June?" % tab, "Hobart", ["Darwin", "Brisbane", "Sydney"], "In winter the far south has the shortest days.")
    return tq("%sWhat pattern does the table show?" % tab, "The further south the city, the bigger the change in day length.",
              ["All cities have the same day length all year.", "Darwin has the biggest change.", "Days are longer in June everywhere."], "Distance from the equator matters.")


TAB = [("Sydney", [("21 December", "5:40 am", "8:05 pm"), ("21 March", "7:05 am", "7:15 pm"), ("21 June", "7:00 am", "4:55 pm"), ("21 September", "5:55 am", "5:55 pm")])]


def g_tab():
    c, rows = TAB[0]
    tab = "<table class='sn-table'><tr><th>Date</th><th>Sunrise</th><th>Sunset</th></tr>%s</table>" % "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in rows)
    k = R.choice(["long", "short", "summer", "winter", "equal"])
    from au_sci import once
    if not once(("tab", k)):
        return None
    if k == "long":
        return tq("%sThe table shows sunrise and sunset in %s (daylight saving ignored for June and September). Which date has the longest day?" % (tab, c),
                  "21 December", ["21 March", "21 June", "21 September"], "From 5:40 am to 8:05 pm is the longest time.")
    if k == "short":
        return tq("%sUsing the table for %s, which date has the shortest day?" % (tab, c), "21 June", ["21 December", "21 March", "21 September"],
                  "From 7:00 am to 4:55 pm is about 10 hours.")
    if k == "summer":
        return tq("%sUsing the table for %s, in which season is the day longest?" % (tab, c), "summer", ["winter", "autumn", "spring"],
                  "21 December is in summer in Australia.")
    if k == "winter":
        return tq("%sUsing the table for %s, how long is the day on 21 June?" % (tab, c), "about 10 hours", ["about 14 hours", "about 12 hours", "about 7 hours"],
                  "7:00 am to 4:55 pm is 9 hours 55 minutes.")
    return tq("%sUsing the table for %s, on which date are day and night closest to equal?" % (tab, c), "21 September",
              ["21 December", "21 June", "the day the Moon is full"], "5:55 am to 5:55 pm is 12 hours (an equinox).")


ROT = [("How long does Earth take to spin once on its axis?", "about 24 hours", ["about 365 days", "about 1 hour", "about 30 days"], "One spin (rotation) is one day."),
       ("How long does Earth take to travel once around the Sun?", "about 365 days", ["about 24 hours", "about 30 days", "about 7 days"], "One orbit (revolution) is one year."),
       ("What causes the seasons?", "Earth's tilted axis as it orbits the Sun", ["Earth getting closer to and further from the Sun", "the Moon's phases", "clouds"], "The tilt changes how directly sunlight hits each place."),
       ("In which direction does the Sun appear to rise?", "the east", ["the west", "the north", "the south"], "Earth spins from west to east."),
       ("When it is summer in Australia, which way is the southern half of Earth tilted?", "towards the Sun", ["away from the Sun", "it has no tilt", "towards the Moon"], "More direct sunlight means warmer weather."),
       ("When it is summer in Australia, what season is it in Europe?", "winter", ["summer", "spring", "the same season"], "The hemispheres have opposite seasons."),
       ("By how many degrees is Earth's axis tilted?", "about 23.5°", ["0°", "90°", "about 45°"], "The tilt stays pointing the same way all year."),
       ("In Australia, when is the midday Sun highest in the sky?", "in summer", ["in winter", "in autumn", "it is the same all year"], "In summer the Sun climbs higher, so shadows are shorter."),
       ("Why are noon shadows shorter in summer than in winter?", "The Sun is higher in the sky in summer.", ["The Sun is closer to Earth in summer.", "Objects grow in summer.", "There is more wind in summer."], "A higher Sun casts a shorter shadow."),
       ("When it is daytime in Australia, where is it night?", "on the other side of Earth, facing away from the Sun", ["nowhere", "everywhere in Australia", "only at the North Pole"], "Half of Earth faces the Sun at any time."),
       ("How many times does Earth spin in one orbit of the Sun?", "about 365 times", ["once", "about 12 times", "about 24 times"], "There are about 365 days in a year."),
       ("Why is it colder in winter even though the Sun shines?", "Sunlight hits the ground at a low angle and days are shorter.", ["The Sun is further away in winter.", "The Sun gives off less light in winter.", "Clouds always block the Sun in winter."], "Low-angle sunlight spreads over a bigger area."),
       ("Which city has the biggest difference in day length between summer and winter?", "Hobart", ["Darwin", "Cairns", "all the same"], "Places further from the equator have bigger changes."),
       ("Near the equator, how much does day length change through the year?", "very little", ["a lot", "it is dark all winter", "it is light all summer"], "Darwin's days stay close to 12 hours."),
       ("What is the longest day of the year in Australia called?", "the summer solstice (around 21 December)", ["the winter solstice (around 21 June)", "the equinox (around 21 March)", "New Year's Day"], "The southern hemisphere is tilted most towards the Sun."),
       ("What is the shortest day of the year in Australia called?", "the winter solstice (around 21 June)", ["the summer solstice (around 21 December)", "the spring equinox", "Australia Day"], "The southern hemisphere is tilted most away from the Sun."),
       ("What is special about the equinoxes in March and September?", "Day and night are about the same length everywhere.", ["It is dark all day.", "The Sun does not rise.", "Earth stops spinning."], "Neither hemisphere leans towards the Sun."),
       ("Why does Antarctica have 24 hours of daylight in December?", "The southern end of Earth is tilted towards the Sun.", ["The Sun is closer to Antarctica.", "Ice makes its own light.", "Earth stops spinning in December."], "Near the poles, the tilt causes very long days in summer."),
       ("What is Earth's axis?", "an imaginary line through the North and South Poles that Earth spins around", ["the path Earth takes around the Sun", "the line between day and night", "the equator"], "Earth rotates around its axis."),
       ("What is the line between day and night on Earth called?", "the terminator", ["the equator", "the axis", "the orbit"], "It moves as Earth spins."),
       ("Which part of Australia sees the sunrise first each day?", "the east coast", ["the west coast", "the centre", "all at the same time"], "Earth spins towards the east."),
       ("Which hemisphere is Australia in?", "the southern hemisphere", ["the northern hemisphere", "both hemispheres equally", "neither hemisphere"], "Australia is south of the equator."),
       ("Which imaginary line divides Earth into the northern and southern hemispheres?", "the equator", ["the axis", "the terminator", "the Tropic of Capricorn"], "The Tropic of Capricorn crosses Australia, south of the equator."),
       ("Which city is closest to the equator?", "Darwin", ["Hobart", "Melbourne", "Adelaide"], "Darwin is in the tropics."),
       ("Why is it hot all year in Darwin?", "It is close to the equator, so the Sun is high in the sky all year.", ["It is closest to the Sun.", "It has no winter clouds.", "It has the longest days in December."], "Near the equator, sunlight is direct all year."),
       ("What would happen if Earth's axis had no tilt?", "There would be almost no seasons.", ["There would be no day and night.", "Earth would stop orbiting.", "Every day would be summer everywhere."], "The tilt causes the seasons."),
       ("Which word describes Earth's path around the Sun?", "orbit", ["axis", "equator", "pole"], "Earth's orbit takes about 365 days.")]
POOL = pool(R, ROT)
POOL5 = pool(R, [
    ("Mia's class measures the length of a stick's shadow every hour from 9 am to 3 pm. What should they keep the same?", "the stick, its position and the way they measure", ["the time of each reading", "the shadow length", "nothing"], "Only the time of day changes."),
    ("Jack draws a graph of noon shadow length each month for a year in Canberra. When will the line be highest?", "in June", ["in December", "in March", "it is flat all year"], "The winter Sun is low, so the shadow is longest."),
    ("Ruby places a sticker on Australia on a globe and turns the globe in front of a lamp. When the sticker faces away from the lamp, what time is it in Australia?", "night", ["midday", "morning", "summer"], "The side facing away from the Sun has night."),
    ("Mia shines a torch on a globe and turns it slowly. What does the torch represent?", "the Sun", ["the Moon", "a star far away", "Earth's core"], "The lit side of the globe has day."),
    ("In Mia's model, what does one full turn of the globe represent?", "one day (24 hours)", ["one year", "one month", "one hour"], "One rotation is one day."),
    ("Jack measures the midday shadow of a 1 m stick in Sydney: 0.3 m in December and 1.4 m in June. Why?", "The midday Sun is higher in December.", ["The Sun is closer in December.", "The stick grew in June.", "June has more sunlight."], "Higher Sun, shorter shadow."),
    ("Ruby says it is hot in summer because Earth is closest to the Sun. What evidence shows she is wrong?", "When Australia has summer, Europe has winter at the same distance from the Sun.", ["Summer is always sunny.", "The Sun is a star.", "Winter is colder."], "Both hemispheres are the same distance from the Sun."),
    ("Kai tilts a globe and moves it around a lamp. What does this model show?", "how the tilt causes seasons as Earth orbits", ["why the Moon has phases", "how volcanoes form", "how clouds form"], "Keep the tilt pointing the same way."),
    ("Ella records sunset times every Monday from January to June in Melbourne. What pattern will she see?", "Sunset gets earlier.", ["Sunset gets later.", "Sunset stays the same.", "The Sun stops setting."], "Days shorten from summer to winter."),
    ("Why do solar panels in Australia usually face north?", "The midday Sun is in the northern part of the sky.", ["The Sun rises in the north.", "North is always cooler.", "Solar panels only work facing north."], "Facing the Sun collects the most light."),
    ("First Nations peoples have many seasons in their calendars, such as six in parts of the Top End. What are these seasons based on?", "changes in weather, plants and animals through the year", ["the days of the week", "the phases of the Moon only", "school terms"], "Observing patterns over many years is science."),
])


def main():
    sets = U.sets([
        ("Day and night", [(POOL, 6), (uk_sky, 3), (uk_turn, 3), (us_dir, 4), (g_rr, 4)]),
        ("Seasons in Australia", [(g_month, 8), (POOL, 5), (g_opp, 5), (g_rr, 2)]),
        ("Tilt and revolution", [(POOL, 6), (g_dl, 3), (g_tab, 5), (g_opp, 4), (us_b1, 2)]),
        ("Day length and the Sun's path", [(g_sp, 8), (g_tab2, 5), (us_graph, 4), (g_dl, 3)]),
        ("Models and evidence", [(POOL5, 8), (POOL, 4), (g_rr, 3), (g_sp, 2), (us_b1, 3)]),
    ])
    make_au(YEAR, "day-night-and-seasons", SORT, "AC9S6U02", "Earth and space sciences",
            "Describe the movement of Earth and other planets relative to the Sun and model how Earth's tilt, rotation on its axis and "
            "revolution around the Sun cause cycles of day and night and seasons (summary of the Australian Curriculum v9.0 Science content description).",
            "Day, Night and Seasons", "Day, night and seasons",
            "Free Year 6 science worksheets on day, night and seasons: Earth's rotation, revolution and tilt, Australian seasons, day length "
            "in Hobart, Sydney and Darwin, and the Sun's height. 100 questions with answers.",
            "Spin gives day and night; tilt gives seasons.", "Earth spins once a day and orbits the Sun once a year with a tilted axis.",
            "<p><b>Earth's rotation causes day and night. Its tilt, as it orbits the Sun, causes the seasons.</b></p><ul>"
            "<li>Earth spins on its axis once every 24 hours. The half facing the Sun has day.</li>"
            "<li>Earth's axis is tilted. From December to February the southern hemisphere leans towards the Sun: Australian summer, longer days and a higher Sun.</li>"
            "<li>From June to August it leans away: winter, shorter days and longer midday shadows. Seasons are not caused by distance from the Sun.</li></ul>",
            [("Which season is July in Australia?", ["June to August is winter in the southern hemisphere"], "winter"),
             ("Why is a midday shadow shorter in December?", ["the Sun is higher in summer"], "the Sun is higher")],
            ["Thinking summer happens because Earth is closer to the Sun.", "Using northern-hemisphere months (Australian summer is December to February).",
             "Mixing up rotation (spin, one day) and revolution (orbit, one year)."],
            [("Why does Australia have summer in December?", "Earth's axis is tilted. In December the southern hemisphere leans towards the Sun, so sunlight is more direct and days are longer."),
             ("What is the difference between rotation and revolution?", "Rotation is Earth spinning on its axis, which takes about 24 hours. Revolution is Earth travelling around the Sun, which takes about 365 days."),
             ("Why does day length change more in Hobart than in Darwin?", "Hobart is much further from the equator. The further a place is from the equator, the bigger the change in day length between summer and winter.")],
            sets, allow=("northern seasons",))


if __name__ == "__main__":
    main()
