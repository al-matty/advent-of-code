"""
Plan:
    Translate input: ('.' -> 0, '@' -> 1)
    Create a numpy array from the input
    get_adjacent_sum(): helper function -> assumes a matrix id, returns the sum of its adjacent cells
    Create a matrix of the result of get_adjacent_sum() applied to each value
    Count the occurences of (value < 4)
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


# Get list of single chars per input line 
with open(in_file) as content:
    content_lines = [list(line.strip()) for line in content.readlines()]

# Translate to list of lists of 0,1 only
summable_list = [[1 if char == '@' else 0 for char in line] for line in content_lines]

# Convert to numpy array
arr = np.array(summable_list)
print(f"Incoming array:\n{arr}")

# Iterate over eles of rows of array, get adjacent sums
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

# Convert back to array & filter based on sum
sum_arr = np.array(list_of_rows)
print(f"\nArray of sums:\n{sum_arr}")

# Return 0 or 1 based on value
filtered_arr = np.where(sum_arr < 4, 1, 0)
print(f"\nFiltered to where val<4:\n{filtered_arr}")

# Add arrays: Keep only positions with 'paper' in the original array (sum=2)
overlaid_arr = arr + filtered_arr
print(f"\nOverlaid array:\n{overlaid_arr}")
final_arr = np.where(overlaid_arr == 2, 1, 0)
print(f"\nFinal array of valid paper roll position:\n{final_arr}")
print(f"\nSum of valid rolls:\n{final_arr.sum()}")