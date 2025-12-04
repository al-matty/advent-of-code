"""
Plan:
    Iterate over part 1 solution:
        Take initial state {arr} and {final_arr} from one iteration
        Add them -> should produce value 2 for each 'taken' paper roll
        Turn each 2 into a 0
        Run again with this as initial state
        Keep count of n_removed
        Stop once sum(final_arr) = 0  <- no more free paper rolls
"""

import numpy as np
in_file = "../data/04_input.txt"

def get_adjacent_sum(in_arr, target_id, x_shape, y_shape):
    """Assumes array, id tuple, arr shape args. Returns sum of adjacent values"""
    x, y = target_id[0], target_id[1]
    # print(f"{target_id}\t<- incoming id tuple")
    
    # Initialize all vals as 0
    r, br, bm, bl, l, ul, u, ur = 0,0,0,0,0,0,0,0
    x_max, y_max = x_shape - 1, y_shape - 1
    
    # Fetch neighbors in all directions
    if y < y_max:
        r = int(in_arr[x, y+1])
    if y < y_max and x < x_max:
        br = int(in_arr[x+1, y+1])
    if x < x_max:
        bm = int(in_arr[x+1, y])
    if y > 0 and x < x_max:
        bl = int(in_arr[x+1, y-1])
    if y > 0:
        l = int(in_arr[x, y-1])
    if y > 0 and x > 0:
        ul = int(in_arr[x-1, y-1])
    if x > 0:
        u = int(in_arr[x-1, y])
    if y < y_max and x > 0:
        ur = int(in_arr[x-1, y+1])
    
    # Return sum of all neighbors
    adjacent_sum = r + br + bm + bl + l + ul + u + ur
    return adjacent_sum


def show_available_for_removal(arr):
    """
    Encapsulates part 1, to be iterated over.
    Returns array of removable paper roll positions (1 = removable, rest 0)
    """
    # Iterate over eles of rows of array, get adjacent sums
    print("="*25)
    print(f"Next iteration. Current state:\n{arr}")
    list_of_rows = []
    arr_length = arr.shape[0]
    arr_width = arr.shape[1]

    for i in range(arr.shape[0]):
        single_row = []
        # print(f"{arr[i]}\t<- current row")
        
        for j in range(arr.shape[1]):

            adj_sum = get_adjacent_sum(arr, (i, j), arr_length, arr_width)
            single_row.append(adj_sum)

        list_of_rows.append(single_row)

    sum_arr = np.array(list_of_rows)                # Convert back to array
    filtered_arr = np.where(sum_arr < 4, 1, 0)      # Return 0 or 1 based on filter
    overlaid_arr = arr + filtered_arr               # Add arrays. Valid eles -> 2
    final_arr = np.where(overlaid_arr == 2, 1, 0)   # Filter to keep only valid

    print(f"\nGenerated array of valid paper roll positions:\n{final_arr}")
    print(f"\nCurrent sum:\n{final_arr.sum()}")

    return final_arr


# Get list of single chars per input line 
with open(in_file) as content:
    content_lines = [list(line.strip()) for line in content.readlines()]

# Translate to list of lists of 0,1 only
summable_list = [[1 if char == '@' else 0 for char in line] for line in content_lines]

# Convert to numpy array
arr = np.array(summable_list)
print(f"Initial array:\n{arr}")

initial_run = True
running_sum = 0

# Iterate & track array sums. Stop when array sum = 0
while True:
    
    arr_to_remove = show_available_for_removal(arr)

    current_sum = arr_to_remove.sum()
    if current_sum == 0:
        break

    # Turn handled paper rows to 0s in the initial array
    overlaid = arr_to_remove + arr
    arr = np.where(overlaid == 2, 0, overlaid)

    running_sum += current_sum

print(f"Final sum: {running_sum}")