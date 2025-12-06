"""
Plan:
    Split input into operands & operators
    Create a matrix from operand cols
    iterate over cols: Collect sum() for '+' and prod() for '*'
"""
import numpy as np

in_file = "../data/06_input_test.txt"
a = np.array([[1,2]])

with open(in_file) as content:
    raw_list = [line.strip() for line in content.readlines()]
    cleanded_list = [line.split() for line in raw_list]  # Remove extra whitespace

# Create arrays
operands = np.array([[int(n) for n in line] for line in cleanded_list[:-1]])
operators = np.array(cleanded_list[-1])
running_sum = 0

for i in range(operands.shape[1]):  # Iterate over columns
    print("Iterating over col", i)
    
    if operators[i] == "+":
        running_sum += operands[:,i].sum()

    if operators[i] == "*":
        running_sum += operands[:,i].prod()

print("Result part 1:", running_sum)
