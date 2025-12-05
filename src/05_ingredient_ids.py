"""
Plan part 1:
    Split input at '\n' -> A = ranges, B = ids
    A) Generate a set from all valid ids based on the ranges
    B) Intersect with id set. Intersection = fresh ids
"""
in_file = "../data/05_input.txt"

# Get range borders as ints
def extract_start_end_tuples(in_str):
    """Return tuples of 2 ints from range strs"""
    return tuple(int(s) for s in in_str.split(sep = "-"))

# Get ranges & ids from file
with open(in_file) as content:
    in_str = content.read()

ranges_str, ids_str = in_str.split("\n\n")[0].strip(), in_str.split("\n\n")[1].strip()
ranges = [line for line in ranges_str.split("\n")]
range_tups = [extract_start_end_tuples(rng_str) for rng_str in ranges]
ids = {int(n_str) for n_str in ids_str.split("\n")}

print(f"\nGot {len(ranges)} ranges and {len(ids)} ids.\n")

# Part 1: Iterate over ids and fill set based on range comparison
valid = set()
for _id in ids:
    #print(f"Running on id {_id}")
    for rng in range_tups:
        #print(rng)
        if rng[0] <= _id <= rng[1]:
            valid.add(_id)


print(f"Part 1: {len(valid)} out of these ids are fresh!")