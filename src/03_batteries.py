#in_file = "../data/03_input_test.txt"
in_file = "data/03_input.txt"
n_digits = 12  # n ints to fetch from strings  


def str_to_int_list(in_str):
    """Convert a str of numbers to a list of ints"""
    return [int(n) for n in ",".join(in_str).split(",")]


def find_max_in_order(in_list, n, ints_to_keep=None):
    """Recursive: Will execute n times, returns n largest ints in order of occurence in in_list"""
    #print(f"Landed inside the top of the recursive function with ints_to_keep {ints_to_keep}")
    
    # Needed to make recursion work. Else list from deafault arg will extend across func calls
    if ints_to_keep is None:
        ints_to_keep = []
    
    # Exit function when n = 0
    if n == 0:
        return ints_to_keep

    # Temporarily remove the last {digits-1} elements from the list to go for largest order of magnitude
    popped_list = in_list
    if n > 1:
        to_pop = n-1
        popped_list = in_list[:-to_pop]

    # Find max int in shortened list
    max_int = max(popped_list)
    ints_to_keep.append(max_int)

    # Drop everything in orig list to its left
    first_max_int_id = in_list.index(max_int)
    in_list = in_list[first_max_int_id+1:]

    # Decrement and call again
    n -= 1
    return find_max_in_order(in_list, n, ints_to_keep)




# Run it on each line of the file input
max_2_per_row = []

with open(in_file) as content:
    battery_strs = [line.strip() for line in content.readlines()]

    for battery_str in battery_strs:
        print(f"Running loop on input {battery_str}")
        battery_list = str_to_int_list(battery_str)

        max_ints = find_max_in_order(battery_list, n_digits)
        print(f"Found max_ints: {max_ints}")
        concatenated = "".join([str(n) for n in max_ints])
        max_2_per_row.append(int(concatenated))

#print(f"Final list: {max_2_per_row}")
print(f"Total: {sum(max_2_per_row)}")