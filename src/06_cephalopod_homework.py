"""
Plan part 1:
    Split input into operands & operators
    Create a matrix from operand cols
    iterate over cols: Collect sum() for '+' and prod() for '*'
Plan part 2:
    create array from whole input incl. operators, 1 char per col
    add reshaping function
        compress/concatenate number strs vertically -> convert to int
        keep list of lists instead of array (different number amounts per group)
    iterate list of lists & operators: Collect sum() for '+' and prod() for '*'
"""
import numpy as np
from math import prod

in_file = "../data/06_input.txt"
part = 2  # 1 or 2


def compress_rows(arr_slice):
    """Take a group of rows, concatenate strings vertically & convert to int"""
    compressed = ["".join(row).strip() for row in arr_slice]
    out_list = [int(n) for n in compressed if n != ""]
    return out_list

def reshape_data(one_char_arr, start_end_tups):
    """Run part 2 concatenation, then reshape to use part 1 logic on data"""
    # Create transposed array without the operators
    transposed = one_char_arr[:-1].T
    operands_list = []

    for tup in start_end_tups:
        #print(f"\nIterationg using ids: [{tup[0]}:{tup[1]}]")
        current_slice = transposed[tup[0]:tup[1]]
        compressed_list = compress_rows(current_slice)
        operands_list.append(compressed_list)
    #[print(x) for x in operands_list[:8]]
    return operands_list

def create_slice_ids(operators_arr):
    """Create start-end-tuples based on operator positions"""
    starts = []
    ends = []
    
    for i in range(len(operators_arr)):
        if operators_arr[i] != " ":
            starts.append(i)

    ends = [start for start in starts][1:]
    ends.append(operators_arr.shape[0])
    
    return list(zip(starts, ends))


# Read data
with open(in_file) as content:
    raw_list = [line.replace("\n", " ") for line in content.readlines()]
    print([len(row) for row in raw_list])

# Create arrays & number group indexes
one_char_list = [[char for char in row] for row in raw_list]
one_char_array = np.array(one_char_list)#[:-1]
operators = one_char_array[-1]
start_end_tups = create_slice_ids(operators)
operators = operators[operators != " "]  # Remove extra cells from operators array

# Part 1
if part == 1:
    cleaned_list = [line.split() for line in raw_list]  # Remove extra whitespace
    operands = np.array([[int(n) for n in line] for line in cleaned_list[:-1]])
    assert operands.shape[1] == operators.shape[0], "That won't fit..."

    # Iterate over columns
    running_sum = 0
    for i in range(operands.shape[1]):
        
        if operators[i] == "+":
            running_sum += operands[:,i].sum()

        if operators[i] == "*":
            running_sum += operands[:,i].prod()

    print(f"Result part {part}:", running_sum)

# Part 2
else:
    operands = reshape_data(one_char_array, start_end_tups)
    assert len(operands) == operators.shape[0], "That won't fit..."

    # Iterate over number groups list of lists & operator array
    running_sum = 0
    for i in range(len(operands)):  # Iterate over columns
        
        if operators[i] == "+":
            running_sum += sum(operands[i])

        if operators[i] == "*":
            running_sum += prod(operands[i])

    print(f"Result part {part}:", running_sum)