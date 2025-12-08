"""
Plan part 1:
    replace initial beam field with "b"
    iterate over rows:
        iterate over position:
            if current row has "." and row above has "b":
                change current row to "b"
            if current row has "^" and row above has "b":
                change l & r to "b" (as long as they are ".")
                increment split counter by 1
Plan part 2:
    Pascal's triangle? -> maybe possibilities can be added up as you go down the tree
    instead of "b", store the number of possible paths at beam points
    create dict of char indexes per line as keys, n outcomes at this point as values
    children nodes inherit the sum of their parents' outcomes
    no split -> no change of possibilities
"""

in_file = "../data/07_input.txt"

# Read data
with open(in_file) as content:
    lines = content.read().splitlines()


# Iterate over each char of each line
split_counter = 0
# dict with indexes as keys, n possibilities at this point as values
beam_possibilities_dict_prior = {}

for i, line in enumerate(lines):

    # Same dict, but for current row
    beam_possibilities_dict_current = {}

    for j, char in enumerate(line):

        if char == "S":  # Set starting value (always 1)
            beam_possibilities_dict_current[j] = 1

        if j in beam_possibilities_dict_prior:
            # Fetch values from last row/state
            n_outcomes_prior = beam_possibilities_dict_prior[j]

            # Case: Normal field: Keep same or add to val from parent
            if char == ".":
                if j in beam_possibilities_dict_current:
                    beam_possibilities_dict_current[j] += n_outcomes_prior
                else:
                    beam_possibilities_dict_current[j] = n_outcomes_prior

            # Case: Splitting field: Add to/set left & right from position
            if char == "^":
                split_counter += 1    # Count splits for part 1
                if line[j-1] == ".":  # Add beam to left
                    if j-1 in beam_possibilities_dict_current:
                        beam_possibilities_dict_current[j-1] += n_outcomes_prior
                    else:
                        beam_possibilities_dict_current[j-1] = n_outcomes_prior

                if line[j+1] == ".":  # Add beam to right
                    if j+1 in beam_possibilities_dict_current:
                        beam_possibilities_dict_current[j+1] += n_outcomes_prior
                    else:
                        beam_possibilities_dict_current[j+1] = n_outcomes_prior

    # Overwrite last row info
    beam_possibilities_dict_prior = beam_possibilities_dict_current 


sum_outcomes = sum([v for v in beam_possibilities_dict_current.values()])
print("\nPart 1 (n splits):", split_counter)
print("Part 2 (n possible paths):", sum_outcomes)