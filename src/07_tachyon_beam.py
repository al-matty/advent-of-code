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
"""

#in_file = "../data/07_input_test.txt"
in_file = "../data/07_input.txt"
part = 1  # 1 or 2


# Read data
with open(in_file) as content:
    lines = content.read().splitlines()

# Part 1
if part == 1:
    
    # Iterate over each char of each line
    split_counter = 0
    beam_positions_last_row = []

    for i, line in enumerate(lines):
        beam_positions_current_row = []

        for j, char in enumerate(line):

            if char == "S":
                beam_positions_current_row.append(j)

            if j in beam_positions_last_row:

                if char == ".":
                    beam_positions_current_row.append(j)

                if char == "^":
                    split_counter += 1

                    if line[j-1] == ".":  # Add beam to left
                        beam_positions_current_row.append(j-1)

                    if line[j+1] == ".":  # Add beam to right
                        beam_positions_current_row.append(j+1)
        # Update last beam positions
        beam_positions_last_row = beam_positions_current_row

    print("Part 1 (n splits):", split_counter)