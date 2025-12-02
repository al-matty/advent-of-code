in_file = "02_input.txt"


# Get number strings
def extract_inclusive_range(in_str):
    # create numbers from range str
    start_end_list = [int(s) for s in in_str.split(sep = "-")]
    n_list = list(range(start_end_list[0], start_end_list[1]+1))
    n_list = [str(n) for n in n_list]
    return n_list

def _has_equal_parts(in_str, pat_size):
    """Check if all slices of size {pat_size} are equal within str"""
    all_slices = {in_str[i:i+pat_size] for i in range(0, len(in_str), pat_size)}

    # Equal slices will produce set size 1
    return len(all_slices) == 1

def check_for_invalid(n_str):
    """Check for increasing slice sizes if a str consist of only the same parts"""
    max_pattern_size = int(len(n_str) / 2)

    # Iterate over string slices of increasing size, until len/2
    for i in range(max_pattern_size):

        pat_size = i+1
        
        # Skip this pattern size if pattern size doesn't add up to string length
        if len(n_str) % pat_size != 0:
            continue

        chunk_1 = n_str[:pat_size]
        chunk_2 = n_str[pat_size:pat_size*2]

        # Compare the first 2 chunks: If equal, do the more expensive test
        if chunk_1 == chunk_2:

            if _has_equal_parts(n_str, pat_size):
                print(f"Found invalid: {n_str}")
    
                return True

    return False


# Read file
with open(in_file) as content:
    in_str = content.read()
    in_list = [n.strip() for n in in_str.split(sep = ",")]


# Iterate and fetch numbers passing the invalid test
inval_ids = []
for rng in in_list:

    n_list = extract_inclusive_range(rng)

    for n_str in n_list:
        if check_for_invalid(n_str):
            inval_ids.append(int(n_str))


print(sum(inval_ids))



# Test data results
# Part 1 correct answer: 24747430309 
# Part 2 correct answer: 4174379265