"""
Plan part 1:
    Split input at '\n' -> A = ranges, B = ids
    Generate range tuples from start and end values
    Compare ids with input range tuples 
Plan part 2:
    Reduce overlapping ranges to as few as possible
    Count from lowest start to higherst end
    Calculate n_gaps and subtract from range count
"""

in_file = "../data/05_input.txt"


def extract_start_end_tuples(in_str):
    """Return tuples of 2 ints from range strs"""
    return tuple(int(s) for s in in_str.split(sep = "-"))

def get_merged_ranges(tup_list):
    """Compress overlapping tuple range list to minimal amount of range tuples"""
    # Sort merge tups based on first value
    tup_list.sort(key=lambda x: x[0])
    print(f"\nIncoming tup_list has {len(tup_list)} range tuples")
    #print(tup_list)

    # Initialize output list ewith first ele from incoming tuple list
    merged_tups = [tup_list[0]]
    #print(merged_tups)

    # Iterate over tuple ranges
    print("Merge iteration...")
    for i in range(1, len(tup_list)):
        current_tup = tup_list[i]
        last_merged = merged_tups[-1]
        #print(f"\tChecking current vs last_merged: {current_tup} <-> {last_merged}")

        # Case: current tuple overlaps or touches last merged tuple -> combine them
        if current_tup[0] <= last_merged[1] + 1:
            #print(f"A: {current_tup[0]} <= {last_merged[1]} + 1  -> merging")
            new_end = max(last_merged[1], current_tup[1])
            combined_tup = (last_merged[0], new_end)
            merged_tups[-1] = combined_tup
            #print(f"Generated combined_tup {combined_tup}")
            #print(f"merged_tups: {merged_tups}")

        # Case: current tuple has gap before it -> append as new range
        else:
            #print(f"B: {current_tup[0]} > {last_merged[1]} + 1  -> gap, appending")
            merged_tups.append(current_tup)
            #print(f"merged_tups: {merged_tups}")

    print(f"Compressed to {len(merged_tups)} merged tuples")
    #print(merged_tups)

    return merged_tups

def calculate_gaps(tup_list):
    """Return number of gaps in between range tuples from list"""
    n_gaps = 0

    for i in range(len(tup_list)):
        if i > 0:
            n_gaps_current = tup_list[i][0] - tup_list[i-1][1] - 1
            n_gaps += n_gaps_current

    return n_gaps 


with open(in_file) as content:
    in_str = content.read()

# Get ranges & ids from file content
ranges_str, ids_str = in_str.split("\n\n")[0].strip(), in_str.split("\n\n")[1].strip()
ranges = [line for line in ranges_str.split("\n")]
range_tups = [extract_start_end_tuples(rng_str) for rng_str in ranges]
ids = {int(n_str) for n_str in ids_str.split("\n")}

print(f"\nGot {len(ranges)} ranges and {len(ids)} ids.\n")
#print(f"\nRange tups: {range_tups}\n")


# Part 1

# Iterate over ids and verify valid ids
valid = set()
for _id in ids:
    #print(f"Running on id {_id}")
    for rng in range_tups:
        #print(rng)
        if rng[0] <= _id <= rng[1]:
            valid.add(_id)

print(f"Part 1: {len(valid)} out of these ids are fresh!")


# Part 2

# Merge into as few complete range tuples as possible
print("Compressing redundant tuple lists...")
merged_tups = get_merged_ranges(range_tups)

# Calculate n gap ids
print("Calculating gaps...")
n_gaps = calculate_gaps(merged_tups)

# Inclusive count from start of first range to end of last
print("Counting number of potential ids...")
gross_count = 1 + merged_tups[-1][1] - merged_tups[0][0]
print("Gross count (before discounting gaps)", gross_count)

# Final count = largest possible range from input - n gaps
net_count = gross_count - n_gaps
print("Final count", net_count)