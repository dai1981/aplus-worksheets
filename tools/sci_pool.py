# Count how many different questions each maker can make: python3 tools/sci_pool.py gen_module g_x g_y (run in tools/)
import sys, importlib, re
sys.path.insert(0, '.')
M = importlib.import_module(sys.argv[1])
import uk_sci
for name in sys.argv[2:]:
    uk_sci.USED.clear()
    f = getattr(M, name); seen = set(); n = 0
    for _ in range(5000):
        try:
            it = f()
        except Exception as e:
            continue
        if it:
            k = (re.sub(r"<[^>]+>", "", it["q"]), it["c"][it["a"]])
            seen.add(k)
    print(name, len(seen))
