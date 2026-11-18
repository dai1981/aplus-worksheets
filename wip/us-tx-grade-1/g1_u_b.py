RESOLVED = '''

def resolved(fn):
    """Picture-answer items are built later with build(pos); build them now at a random position."""
    def f(rnd):
        st = fn(rnd)
        st["items"] = [it["build"](rnd.randrange(4)) if "build" in it else it for it in st["items"]]
        return st
    f.__name__ = fn.__name__
    return f
'''

unit(fname="shapes_2d", slug="2d-shapes", sort=14, domain=GM, code="1.6A, 1.6C, 1.6D, 1.6F", seed=69114,
  title="2D Shapes: Sides, Vertices and Attributes", short="2D Shapes",
  doc="Naming shapes, counting sides and vertices, what matters and what does not, and putting shapes together (the US\nGrade 1 makers with Texas names), plus describing circles, triangles, rectangles, squares, rhombuses and hexagons\n(own maker).\nWrong answers come from real mistakes: naming a shape by its color or size, counting a side twice, and thinking a\nsquare is not a rectangle.",
  imports=mods(("gen_us_math_g1_shapes", "sh")),
  extra=UNIQ + '''
ATTR = [("circle", "It is round. It has no sides and no vertices."), ("triangle", "It has 3 straight sides and 3 vertices."),
        ("rectangle", "It has 4 straight sides and 4 square corners."), ("square", "It has 4 sides that are all the same length and 4 square corners."),
        ("rhombus", "It has 4 sides that are all the same length, but its corners are not square."), ("hexagon", "It has 6 straight sides and 6 vertices.")]
FACT = [("Is a square a special rectangle?", "Yes, it has 4 square corners", ["No, it is too small", "No, it has 3 sides", "Yes, it is round"], "A square has 4 square corners, so it is a special <b>rectangle</b> with all sides the same."),
        ("How many vertices does a circle have?", "0", ["1", "4", "2"], "A circle is round. It has <b>0</b> vertices."),
        ("Which shape has 6 sides?", "Hexagon", ["Rhombus", "Triangle", "Rectangle"], "A <b>hexagon</b> has 6 sides."),
        ("Which shape has all sides the same length but no square corners?", "Rhombus", ["Rectangle", "Circle", "Triangle"], "A <b>rhombus</b> has 4 equal sides; its corners are not square."),
        ("What is a vertex?", "A corner where two sides meet", ["A curved line", "The inside of a shape", "A long side"], "A <b>vertex</b> is where two sides meet."),
        ("Two triangles are put together to make a square. How many sides does the square have?", "4", ["3", "6", "2"], "A square has <b>4</b> sides."),
        ("How many triangles of the same size can make a hexagon?", "6", ["2", "3", "4"], "<b>6</b> triangles fit together to make a hexagon.")]


def one_attr(r):
    name, clue = r.choice(ATTR)
    others = [n for n, c in ATTR if n != name]
    return mcq("%s Which shape is it?" % clue, name[0].upper() + name[1:], [x[0].upper() + x[1:] for x in r.sample(others, 3)], "%s That is a <b>%s</b>." % (clue, name))


def one_fact(r):
    q, a, w, e = r.choice(FACT)
    return mcq(q, a, w, e)
''',
  specs='''        ("Name the shape", [("run", sh.set_name, ("rnd", sh.People), 20)]),
        ("Count sides and vertices", [("run", sh.set_count, ("rnd", sh.People), 20)]),
        ("Describe the shape", [("collect", uniq(one_attr), 6), ("collect", uniq(one_fact), 7), ("run", sh.set_name, ("rnd", sh.People), 7)]),
        ("What makes a shape that shape?", [("run", sh.set_matters, ("rnd", sh.People), 20)]),
        ("Put shapes together", [("run", sh.set_compose, ("rnd", sh.People), 20)]),''',
  think="<ul><li>Count the <b>sides</b> (straight lines) and the <b>vertices</b> (corners).</li><li>Triangle 3, rectangle 4, square 4, rhombus 4, hexagon 6. A circle has none.</li><li>A <b>square</b> is a special rectangle with all sides the same.</li><li>Color, size and how a shape is turned do <b>not</b> change its name.</li></ul>",
  examples='example("4 equal sides, square corners", ["4 sides, 4 vertices"], "square")',
  mistakes=[["Naming a shape by its color or size", "A big blue triangle is still a triangle."], ["Counting a side twice", "Start at one side and go around once."], ["Thinking a square is not a rectangle", "A square has 4 square corners."]],
  faq=[("What does TEKS 1.6D ask?", "Identify two-dimensional shapes, including circles, triangles, rectangles, and squares as special rectangles, rhombuses, and hexagons and describe their attributes using formal geometric language."), ("What does TEKS 1.6A ask?", "Classify and sort regular and irregular two-dimensional shapes based on attributes using informal geometric language."), ("What does TEKS 1.6F ask?", "Compose two-dimensional shapes by joining two, three, or four figures to produce a target figure in more than one way if possible."), ("Does turning a shape change its name?", "No.")],
  std="1.6A classify and sort regular and irregular two-dimensional shapes based on attributes using informal geometric language; 1.6C create two-dimensional figures, including circles, triangles, rectangles, and squares, as special rectangles, rhombuses, and hexagons; 1.6D identify two-dimensional shapes, including circles, triangles, rectangles, and squares as special rectangles, rhombuses, and hexagons and describe their attributes using formal geometric language; 1.6F compose two-dimensional shapes by joining two, three, or four figures to produce a target figure in more than one way if possible",
  meta="Free Grade 1 2D shape worksheets for Texas TEKS 1.6A, 1.6C, 1.6D and 1.6F: name shapes, count sides and vertices, describe attributes and put shapes together. 100 questions with answers.",
  kb="Count sides and vertices to name a shape.", ks="Triangle 3, square 4, hexagon 6, circle 0.", seo="Grade 1 2D Shapes Worksheets: Sides and Vertices (TEKS 1.6D)")

unit(fname="solids_3d", slug="3d-solids", sort=15, domain=GM, code="1.6B, 1.6E", seed=69115,
  title="3D Solids: Spheres, Cones, Cylinders and Prisms", short="3D Solids",
  doc="Naming solids (the US Grade 1 maker), solid clues and real objects (the Texas Grade 2 makers), cubes and faces of\nsolids (US Grade 2 and Ontario makers), and what does and does not make a solid (own maker), all with Texas names.\nWrong answers come from real mistakes: mixing up 2D and 3D names, and naming a solid by its color or size.",
  imports=mods(("gen_us_math_g1_shapes", "sh"), ("gen_us_math_g2_shapes", "sh2"), ("gen_caon_math_g3_shapes", "csh")) + "\nimport gen_ustx_math_g2_solids_3d as s3",
  extra=UNIQ + '''
DEF = [("A cube is painted red. Does the color make it a cube?", "No, it has 6 square faces", ["Yes, all cubes are red", "Yes, red makes it a cube", "No, cubes have no faces"], "A cube is a cube because of its <b>6 square faces</b>, not its color."),
       ("A big ball and a small marble are both spheres. Why?", "Both are round all over", ["Both are big", "Both are red", "Both have flat faces"], "Size does not matter. Both are <b>round all over</b>."),
       ("A cone is turned upside down. Is it still a cone?", "Yes", ["No, it is a cylinder", "No, it is a sphere", "Only if it is red"], "Turning a solid does not change its name. It is still a <b>cone</b>."),
       ("Which tells you a solid is a cylinder?", "2 flat circle faces and a curved surface", ["It is blue", "It is tall", "It is made of metal"], "A cylinder has <b>2 flat circle faces</b> and a curved surface."),
       ("Which does NOT matter when you name a solid?", "Its color", ["The shape of its faces", "The number of faces", "If it has a curved surface"], "<b>Color</b> does not change the name of a solid."),
       ("Which tells you a solid is a triangular prism?", "2 triangle faces and 3 rectangle faces", ["It is yellow", "It is small", "It can be held in one hand"], "A triangular prism has <b>2 triangle faces and 3 rectangle faces</b>."),
       ("Which solid has a point at the top and a circle face at the bottom?", "A cone", ["A cylinder", "A cube", "A sphere"], "That is a <b>cone</b>."),
       ("Which solid has 6 faces that are rectangles?", "A rectangular prism", ["A cone", "A sphere", "A cylinder"], "A <b>rectangular prism</b> has 6 rectangle faces.")]


def one_def(r):
    q, a, w, e = r.choice(DEF)
    return mcq(q, a, w, e)
''',
  specs='''        ("Name the solid", [("run", sh.set_solids, ("rnd", sh.People), 20)]),
        ("Solids in the world", [("collect", uniq(s3.one_clue), 6), ("collect", uniq(s3.one_real), 14)]),
        ("Cubes: faces, edges and vertices", [("run", sh2.set_cube, ("rnd", sh2.People), 20)]),
        ("Faces of solids", [("run", csh.set_faces, ("rnd", csh.People), 20)]),
        ("What makes a solid that solid?", [("collect", uniq(one_def), 8), ("collect", uniq(s3.one_sort), 7), ("collect", uniq(s3.one_cmp), 5)]),''',
  think="<ul><li>3D <b>solids</b>: sphere, cone, cylinder, rectangular prism, cube, triangular prism.</li><li>A <b>face</b> is a flat surface. A sphere has none.</li><li>A <b>cube</b> is a rectangular prism with 6 square faces.</li><li>Color, size and how a solid is turned do <b>not</b> change its name.</li></ul>",
  examples='example("A can of soup", ["2 circle faces, curved surface"], "cylinder")',
  mistakes=[["Mixing up 2D and 3D names", "A circle is flat; a sphere is a ball."], ["Naming a solid by its color or size", "A small red cube is still a cube."], ["Calling a cube a square", "A square is one face of a cube."]],
  faq=[("What does TEKS 1.6E ask?", "Identify three-dimensional solids, including spheres, cones, cylinders, rectangular prisms (including cubes), and triangular prisms, and describe their attributes using formal geometric language."), ("What does TEKS 1.6B ask?", "Distinguish between attributes that define a two-dimensional or three-dimensional figure and attributes that do not define the shape."), ("Is a cube a rectangular prism?", "Yes. It is a special one with square faces."), ("Which solids can roll?", "Spheres, cones and cylinders.")],
  std="1.6B distinguish between attributes that define a two-dimensional or three-dimensional figure and attributes that do not define the shape; 1.6E identify three-dimensional solids, including spheres, cones, cylinders, rectangular prisms (including cubes), and triangular prisms, and describe their attributes using formal geometric language",
  meta="Free Grade 1 3D solid worksheets for Texas TEKS 1.6B and 1.6E: spheres, cones, cylinders, cubes and prisms, faces, and what does and does not make a solid. 100 questions with answers.",
  kb="Name a solid by its faces, not its color.", ks="A cube has 6 square faces.", seo="Grade 1 3D Solids Worksheets (TEKS 1.6E)")

unit(fname="halves_fourths", slug="halves-and-fourths", sort=16, domain=GM, code="1.6G, 1.6H", seed=69116,
  title="Halves and Fourths: Equal Parts", short="Halves and Fourths",
  doc="Halves, fourths, equal or not equal shares, which part is shaded, and sharing stories (the US Grade 1 makers).\nWrong answers come from real mistakes: calling unequal parts halves, counting parts that are not the same size, and\nthinking more parts means bigger parts.",
  imports=mods(("gen_us_math_g1_halves_fourths", "hf")),
  extra=RESOLVED,
  specs='''        ("Halves", [("run", resolved(hf.set_halves), ("rnd",), 20)]),
        ("Fourths and quarters", [("run", resolved(hf.set_fourths), ("rnd",), 20)]),
        ("Equal or not equal shares?", [("run", resolved(hf.set_equal), ("rnd",), 20)]),
        ("What part is shaded?", [("run", resolved(hf.set_shaded), ("rnd",), 20)]),
        ("Bigger or smaller? Sharing stories", [("run", resolved(hf.set_stories), ("rnd",), 20)]),''',
  think="<ul><li><b>Halves</b>: 2 equal parts. Each part is one half.</li><li><b>Fourths</b> (quarters): 4 equal parts. Each part is one fourth.</li><li>The parts must be the <b>same size</b>.</li><li>More equal parts means smaller parts: a fourth is smaller than a half.</li></ul>",
  examples='example("A pizza cut into 4 equal parts", ["4 equal parts"], "fourths")',
  mistakes=[["Calling unequal parts halves", "Halves must be the same size."], ["Counting parts that are not equal", "Check that each part is the same size."], ["Thinking a fourth is bigger than a half", "More parts means smaller parts."]],
  faq=[("What does TEKS 1.6G ask?", "Partition two-dimensional figures into two and four fair shares or equal parts and describe the parts using words."), ("What does TEKS 1.6H ask?", "Identify examples and non-examples of halves and fourths."), ("Is a quarter the same as a fourth?", "Yes."), ("Which is bigger, a half or a fourth of the same pizza?", "A half.")],
  std="1.6G partition two-dimensional figures into two and four fair shares or equal parts and describe the parts using words; 1.6H identify examples and non-examples of halves and fourths",
  meta="Free Grade 1 halves and fourths worksheets for Texas TEKS 1.6G and 1.6H: equal parts, examples and non-examples, shaded parts and sharing stories. 100 questions with answers.",
  kb="Halves are 2 equal parts; fourths are 4 equal parts.", ks="A fourth is smaller than a half.", seo="Grade 1 Halves and Fourths Worksheets (TEKS 1.6G)")

unit(fname="measuring_length", slug="measuring-length", sort=17, domain=GM, code="1.7A, 1.7B, 1.7C, 1.7D", seed=69117,
  title="Measuring Length with Units", short="Measuring Length",
  doc="Measuring with cubes and paper clips, measuring the right way (no gaps or overlaps), two different units, ordering\nby length, and how many longer (the US Grade 1 and Grade 2 makers with Texas names).\nWrong answers come from real mistakes: leaving gaps, starting past the end, and thinking a bigger unit gives a\nbigger number.",
  imports=mods(("gen_us_math_g1_measuring", "me"), ("gen_us_math_g2_measuring", "me2")),
  specs='''        ("Measure with cubes and paper clips", [("run", me.set_units, (me.People,), 20)]),
        ("Measure the right way", [("run", me.set_right_way, (me.People,), 20)]),
        ("Two different units", [("run", me2.set_two_units, (me2.People,), 20)]),
        ("Order by length", [("run", me.set_order, (me.People,), 20)]),
        ("How many longer?", [("run", me.set_word, (me.People,), 20)]),''',
  think="<ul><li>Lay same-size units <b>end to end</b>. No gaps. No overlaps.</li><li>Start at one end and stop at the other end.</li><li>Say the number and the unit: 6 cubes long.</li><li>Bigger units: fewer of them. Smaller units: more of them.</li></ul>",
  examples='example("A pencil is 6 cubes long", ["Count the cubes end to end"], "6 cubes")',
  mistakes=[["Leaving gaps", "Units must touch."], ["Starting past the end", "Line up the first unit with the end."], ["Thinking bigger units give a bigger number", "Bigger units mean fewer units."]],
  faq=[("What does TEKS 1.7B ask?", "Illustrate that the length of an object is the number of same-size units of length that, when laid end-to-end with no gaps or overlaps, reach from one end of the object to the other."), ("What does TEKS 1.7C ask?", "Measure the same object/distance with units of two different lengths and describe how and why the measurements differ."), ("What does TEKS 1.7D ask?", "Describe a length to the nearest whole unit using a number and a unit."), ("What does TEKS 1.7A ask?", "Use measuring tools to measure the length of objects to reinforce the continuous nature of linear measurement.")],
  std="1.7A use measuring tools to measure the length of objects to reinforce the continuous nature of linear measurement; 1.7B illustrate that the length of an object is the number of same-size units of length that, when laid end-to-end with no gaps or overlaps, reach from one end of the object to the other; 1.7C measure the same object/distance with units of two different lengths and describe how and why the measurements differ; 1.7D describe a length to the nearest whole unit using a number and a unit",
  meta="Free Grade 1 measuring worksheets for Texas TEKS 1.7A–1.7D: measure with cubes and paper clips, no gaps or overlaps, two different units and comparing lengths. 100 questions with answers.",
  kb="Units end to end: no gaps, no overlaps.", ks="Bigger units, fewer units.", seo="Grade 1 Measuring Length Worksheets (TEKS 1.7B)")

unit(fname="time", slug="telling-time-to-the-hour-and-half-hour", sort=18, domain=GM, code="1.7E", seed=69118,
  title="Telling Time to the Hour and Half Hour", short="Time to the Hour and Half Hour",
  doc="Time to the hour and to the half hour, matching analog and digital clocks, where the hands point, and time in daily\nlife (the US Grade 1 makers with Texas names).\nWrong answers come from real mistakes: mixing up the hands, reading the hour wrong at half past, and writing 3:30 as\n3:00.",
  imports=mods(("gen_us_math_g1_time", "tm")),
  specs='''        ("Time to the hour", [("run", tm.set_hour, ("rnd",), 20)]),
        ("Time to the half hour", [("run", tm.set_half, ("rnd",), 20)]),
        ("Match clocks", [("run", tm.set_match, ("rnd",), 20)]),
        ("Where do the hands point?", [("run", tm.set_hands, ("rnd",), 20)]),
        ("Time in daily life", [("run", tm.set_life, ("rnd", tm.People), 20)]),''',
  think="<ul><li>The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes.</li><li>Long hand on 12: o'clock (3:00).</li><li>Long hand on 6: half past (3:30). The short hand is halfway between 3 and 4.</li></ul>",
  examples='example("Short hand between 3 and 4, long hand on 6", ["half past 3"], "3:30")',
  mistakes=[["Mixing up the hands", "The short hand is the hour."], ["Reading the next hour at half past", "Use the number the short hand has passed."], ["Writing half past 3 as 3:00", "Half past is :30."]],
  faq=[("What does TEKS 1.7E ask?", "Tell time to the hour and half hour using analog and digital clocks."), ("What does half past mean?", "30 minutes after the hour."), ("Where is the long hand at 7:00?", "On the 12."), ("Where is the short hand at 7:30?", "Halfway between 7 and 8.")],
  std="1.7E tell time to the hour and half hour using analog and digital clocks",
  meta="Free Grade 1 time worksheets for Texas TEKS 1.7E: tell time to the hour and half hour on analog and digital clocks. 100 questions with answers.",
  kb="Long hand on 12: o'clock. On 6: half past.", ks="Half past 3 is 3:30.", seo="Grade 1 Telling Time to the Hour and Half Hour Worksheets (TEKS 1.7E)")

unit(fname="graphs", slug="tally-marks-and-graphs", sort=19, domain=DA, code="1.8A, 1.8B, 1.8C", seed=69119,
  title="Tally Marks, Picture Graphs and Bar Graphs", short="Tally Marks and Graphs",
  doc="Sorting and counting, tally charts, picture graphs, bar graphs, and how many in all, more and fewer (the US Grade 1\nmakers with Texas names).\nWrong answers come from real mistakes: counting a bundle of tallies as 1, reading the wrong row, and adding when the\nquestion asks how many more.",
  imports=mods(("gen_us_math_g1_data", "da")),
  specs='''        ("Sort and count", [("run", da.set_sort, ("rnd",), 20)]),
        ("Read tally charts", [("run", da.set_tally, ("rnd", da.Picker), 20)]),
        ("Read picture graphs", [("run", da.set_picture, ("rnd", da.Picker), 20)]),
        ("Read bar graphs", [("run", da.set_bar, ("rnd", da.Picker), 20)]),
        ("How many in all, how many more, how many fewer", [("run", da.set_word, ("rnd", da.Picker), 20)]),''',
  think="<ul><li><b>Sort</b> things into groups, then count each group.</li><li>A <b>tally mark</b> is 1. A bundle of 5 tallies (four lines and one across) is 5.</li><li>In a <b>picture graph</b>, count the pictures. In a <b>bar graph</b>, read the number at the end of the bar.</li><li>How many more: subtract. In all: add.</li></ul>",
  examples='example("Tally: one bundle and 2 more", ["5 + 2"], "7")',
  mistakes=[["Counting a bundle of tallies as 1", "A bundle is 5."], ["Reading the wrong row", "Put your finger on the label first."], ["Adding when asked how many more", "How many more means subtract."]],
  faq=[("What does TEKS 1.8A ask?", "Collect, sort, and organize data in up to three categories using models/representations such as tally marks or T-charts."), ("What does TEKS 1.8B ask?", "Use data to create picture and bar-type graphs."), ("What does TEKS 1.8C ask?", "Draw conclusions and generate and answer questions using information from picture and bar-type graphs."), ("Why cross the fifth tally?", "It makes groups of 5 easy to count.")],
  std="1.8A collect, sort, and organize data in up to three categories using models/representations such as tally marks or T-charts; 1.8B use data to create picture and bar-type graphs; 1.8C draw conclusions and generate and answer questions using information from picture and bar-type graphs",
  meta="Free Grade 1 data worksheets for Texas TEKS 1.8: sort and count, tally charts, picture graphs, bar graphs and how many more or fewer. 100 questions with answers.",
  kb="Count tallies by 5s, then 1s.", ks="One bundle and 2 more is 7.", seo="Grade 1 Tally Marks and Graphs Worksheets (TEKS 1.8)")
