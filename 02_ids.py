in_file = "02_input.txt"

# Read file
with open(in_file) as content:
    in_str = content.read()
    in_list = [n.strip() for n in in_str.split(sep = ",")]

# Get number strings
def extract_inclusive_range(in_str):
    # create numbers from range str
    start_end_list = [int(s) for s in in_str.split(sep = "-")]
    n_list = list(range(start_end_list[0], start_end_list[1]+1))
    n_list = [str(n) for n in n_list]
    return n_list

# Test 1
def is_mirror_number(in_str):
    if len(in_str) % 2 == 0:
        return True

# Test 2
def has_equal_parts(in_str):
    mid_pos = int(len(in_str) / 2)
    part_1 = in_str[:mid_pos]
    part_2 = in_str[mid_pos:]

    if part_1 == part_2:
        return True


inval_ids = []

# Iterate and fetch numbers passing both tests
for rng in in_list:

    n_list = extract_inclusive_range(rng)

    for n_str in n_list:
        if is_mirror_number(n_str):
            if has_equal_parts(n_str):
                inval_ids.append(int(n_str))

print(sum(inval_ids))

