# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 1, AC9S1U02: daily and seasonal changes in the environment - day and night, the weather,
the four seasons in southern Australia and the wet and dry seasons in the north, and how these changes affect what we do.
  python tools/gen_au_science_y1_daily_and_seasonal_changes.py
Reuses the UK Year 1 weather and seasons makers and the US Kindergarten weather makers with Australian names (month and season
questions from the northern hemisphere are dropped), plus own questions on Australian seasons. Short sentences.
Wrong answers come from real mistakes: putting Christmas in winter, thinking the Sun goes away at night, and mixing up weather and seasons.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once, keep
import json
import sci_kids as K

YEAR, SORT = 1, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

WD = "gen_uk_science_y1_weather_and_day_length"
FS = "gen_uk_science_y1_four_seasons"
KW = "gen_us_science_gk_weather"
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December",
       "Christmas", "Easter", "Halloween", "snowman", "sledge", "snow day", "conker", "longest day", "shortest day", "day length", "sunset", "sunrise", "bonfire", "snow", "mitten"]
NOSNOW = lambda it: "snow" not in json.dumps(it).lower()
w_chart = limit(keep(src(WD, "g_chart", drop=MON), NOSNOW), 6)
w_desc = src(WD, "g_desc", drop=MON)
w_do = src(WD, "g_do", drop=MON)
w_sym = keep(src(WD, "g_sym", drop=MON), NOSNOW)
w_b1 = src.B(WD, "B1", drop=MON)
f_temp = limit(src(FS, "g_temp", drop=MON), 5)
f_wear = src(FS, "g_wear", drop=MON)
k_week = limit(keep(src(KW, "g_week", drop=MON), NOSNOW), 5)
k_word = src(KW, "g_word", drop=MON)
k_clue = src(KW, "g_clue", drop=MON)
k_wear = src(KW, "g_wear", drop=MON)
k_b5 = src.B(KW, "B5", drop=MON)

SEASON = [("summer", "December, January and February", "hot", "swimming at the beach"),
          ("autumn", "March, April and May", "cooler, and some leaves change colour", "raking leaves"),
          ("winter", "June, July and August", "cold", "wearing a warm jumper"),
          ("spring", "September, October and November", "warmer, and many flowers bloom", "seeing baby birds")]


def g_season():
    s, m, w, act = R.choice(SEASON)
    k = R.choice(["months", "weather", "act"])
    if not once(("ss", s, k)):
        return None
    if k == "months":
        return tq("In southern Australia, which months are %s?" % s, m, [x[1] for x in SEASON if x[0] != s], "In Australia, summer starts in December.")
    if k == "weather":
        return tq("What is the weather usually like in %s in Melbourne?" % s, w, [x[2] for x in SEASON if x[0] != s], "Each season has its own weather.")
    return tq("Which season is best for %s?" % act, s, [x[0] for x in SEASON if x[0] != s], "Seasons change what we do.")


ORDER = ["summer", "autumn", "winter", "spring"]
EVENT = [("Australia Day (26 January)", "summer"), ("Anzac Day (25 April)", "autumn"), ("the start of the year in June", "winter"),
         ("the footy finals in September", "spring"), ("Melbourne Cup Day in November", "spring"), ("New Year's Day (1 January)", "summer")]


def g_order():
    i = R.randrange(4)
    k = R.choice(["after", "before", "event"])
    if not once(("or", i, k)):
        return None
    if k == "after":
        a = ORDER[(i + 1) % 4]
        return tq("Which season comes after %s?" % ORDER[i], a, [x for x in ORDER if x != a], "Summer → autumn → winter → spring.")
    if k == "before":
        a = ORDER[(i - 1) % 4]
        return tq("Which season comes before %s?" % ORDER[i], a, [x for x in ORDER if x != a], "Summer → autumn → winter → spring.")
    ev, a = EVENT[i]
    if "June" in ev:
        ev, a = EVENT[4]
    return tq("In southern Australia, which season is %s in?" % ev, a, [x for x in ORDER if x != a], "Summer is December to February.")


DRESS = [("hot and sunny", "a hat, sunscreen and a T-shirt"), ("cold and frosty", "a jumper, a beanie and long pants"),
         ("rainy", "a raincoat and gumboots"), ("windy", "a jacket zipped up"), ("stormy with lightning", "stay inside")]


def g_dress():
    w, a = R.choice(DRESS)
    who = R.choice(["Mia", "Jack", "Ruby", "Kai", "Ella", "Noah"])
    if not once(("dr", w, who)):
        return None
    return tq("It is %s. What should %s do or wear?" % (w, who), a, [x[1] for x in DRESS if x[1] != a][:3], "Dress for the weather.")


DN = [("see the Sun in the sky", "day"), ("see lots of stars", "night"), ("eat breakfast", "day"), ("go to bed", "night"),
      ("see an owl hunting", "night"), ("see possums looking for food", "night"), ("play at lunch time", "day"),
      ("see the Moon and stars clearly", "night"), ("see kookaburras laughing at dawn", "day"), ("see bats flying out to feed", "night"),
      ("see the Sun high in the sky", "day"), ("turn on the lights to see", "night")]


def g_dn():
    act, a = R.choice(DN)
    if not once(("dn", act)):
        return None
    return tq("When do we usually %s?" % act, "at %s" % a if a == "night" else "in the %s" % a,
              ["at night" if a == "day" else "in the day", "never", "only in winter"], "Day is light; night is dark.")


POOL1 = pool(R, [
    ("In Australia, which season is Christmas in?", "summer", ["winter", "autumn", "spring"], "Many families go to the beach at Christmas."),
    ("Why is it dark at night?", "Our side of the Earth is turned away from the Sun.", ["The Sun turns off.", "The Moon covers the Sun.", "Clouds cover the Sun."], "The Earth spins once each day."),
    ("When is the Sun highest in the sky?", "around the middle of the day", ["at night", "early in the morning", "at sunset"], "Shadows are shortest at midday."),
    ("What do we see in the sky at night?", "the Moon and stars", ["only the Sun", "rainbows", "nothing"], "Sometimes we can see the Moon in the day too."),
    ("In northern Australia, such as Darwin, what are the two main seasons?", "the wet season and the dry season", ["only winter", "snow and ice", "spring and autumn only"], "First Nations peoples describe even more seasons."),
    ("What should you wear on a hot sunny day?", "a hat, sunscreen and light clothes", ["a thick coat and gloves", "a raincoat and gumboots", "a woolly scarf"], "Slip, slop, slap!"),
    ("What should you take on a rainy day?", "an umbrella or a raincoat", ["sunglasses only", "a beach towel", "a fan"], "Stay dry."),
    ("What is the weather?", "what it is like outside today, such as sunny, rainy or windy", ["the time of day", "the name of a season", "a type of animal"], "Weather can change quickly."),
    ("Which tool measures how hot it is?", "a thermometer", ["a ruler", "a clock", "a scale"], "Temperature is measured in degrees Celsius (°C)."),
    ("What happens to many animals at night?", "some sleep and some, like possums and owls, wake up", ["all animals sleep", "all animals wake up", "nothing changes"], "Animals active at night are nocturnal."),
    ("Why do we wear more clothes in winter?", "It is cold and we need to stay warm.", ["To look tall.", "Because it is hot.", "To keep the rain away only."], "Seasons change what we wear."),
    ("What happens in the morning?", "the Sun rises and it gets light", ["the Sun sets", "it gets dark", "the stars come out"], "Day starts at sunrise."),
])
POOL5 = pool(R, [
    ("Mia records the weather each day for a week. How can she show it?", "draw a weather chart with symbols", ["guess the weather", "only write the date", "count the clouds once"], "Charts help us see patterns."),
    ("Jack measures the temperature at 9 am and at 1 pm. Which is usually warmer?", "1 pm", ["9 am", "both the same", "neither"], "It gets warmer as the Sun rises higher."),
    ("Ruby draws around her shadow at 9 am and at noon. When is her shadow shorter?", "at noon", ["at 9 am", "both the same", "she has no shadow"], "The Sun is higher at noon."),
    ("Kai counts rainy days each month in Darwin. When will he count the most?", "in the wet season (around January)", ["in the dry season (around July)", "all months the same", "never"], "Darwin has a wet and a dry season."),
    ("Ella puts a rain gauge in the garden. What does it measure?", "how much rain falls", ["how hot it is", "how windy it is", "the time"], "Rainfall is measured in millimetres."),
    ("Noah watches a gum tree's shadow during the day. What happens to it?", "it moves and changes length", ["it stays still", "it disappears forever", "it turns blue"], "The Sun moves across the sky."),
])


def main():
    sets = U.sets([
        ("Day and night", [(g_dn, 10), (POOL1, 5), (w_do, 3), (w_b1, 2)]),
        ("Weather", [(w_desc, 5), (w_sym, 4), (k_word, 3), (k_clue, 3), (POOL1, 2), (g_dress, 3)]),
        ("The seasons in Australia", [(g_season, 10), (g_order, 6), (POOL1, 2), (f_temp, 2), (f_wear, 2)]),
        ("Weather charts", [(w_chart, 6), (k_week, 5), (f_temp, 2), (POOL1, 1), (g_dress, 4), (k_wear, 2)]),
        ("Changes and what we do", [(POOL5, 6), (k_b5, 3), (g_dress, 5), (g_dn, 2), (POOL1, 1), (g_season, 1), (k_wear, 2)]),
    ])
    pic = K.row(["sun", "rain", "wind", "moon"], words=["sunny", "rainy", "windy", "night"], size=80, label="sunny, rainy and windy weather and the night")
    make_au(YEAR, "daily-and-seasonal-changes", SORT, "AC9S1U02", "Earth and space sciences",
            "Describe daily and seasonal changes in the environment and explore how these changes affect everyday life "
            "(summary of the Australian Curriculum v9.0 Science content description).",
            "Daily and Seasonal Changes", "Day, weather and seasons",
            "Free Year 1 science worksheets on daily and seasonal changes: day and night, weather, the four seasons in Australia, the "
            "wet and dry seasons, and weather charts. 100 questions with answers.",
            "Weather and seasons change.", "Day turns to night. In southern Australia, summer is in December and winter is in June.",
            ("The sky and weather change.", ["Day and night change every day.", "Weather can be sunny, rainy or windy.",
                                             "Summer is hot; winter is cold."]),
            [("Which season is Christmas in Australia?", ["December is summer"], "summer")],
            ["Putting Christmas in winter (it is summer in Australia).", "Thinking the Sun turns off at night."],
            [("What are the seasons in Australia?", "Most of Australia has summer (December to February), autumn, winter (June to August) and spring. The north has a wet season and a dry season."),
             ("What is the difference between weather and seasons?", "Weather is what it is like outside today. Seasons are times of the year with their own usual weather."),
             ("How can children track the weather?", "Keep a weather chart with a symbol for each day, and measure rain or temperature.")],
            sets, pic=pic, allow=("northern seasons",))


if __name__ == "__main__":
    main()
