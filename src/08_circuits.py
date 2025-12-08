"""
Plan part 1:
    create distance matrix of all points
    create a second FALSE matrix to keep track of what's been handled already
    circuits  <- list of id sets (1 set = one "circuit")
        
    make 1000 connections (always use smallest distance):
        find id pair of min value in distance matrix (= closest pair)
            if both ids new: create a new "circuit" set, add to circuits
            if one id part of a circuit already: add the new one to that set
            if neither id is new & not in same set: merge sets
        update matrix to ignore point pairs that have been handled already
    sort list by set size (lambda len)
    take first 3-item-slice, multiply lengths
"""

import numpy as np
from math import prod
from scipy.spatial import distance_matrix

#in_file = "../data/08_input_test.txt"
in_file = "../data/08_input.txt"

# Read data
with open(in_file) as content:
    lines = content.read().splitlines()

# Create coordinates array
points = [[int(coord) for coord in line.split(",")] for line in lines]    
points_arr = np.array(points)
print(points_arr)

# Create eucl distance matrix
eucl_distances = distance_matrix(points_arr, points_arr)
print(f"\ncreated initial distances matrix of shape {eucl_distances.shape}")

 # Create bool mask for keeping track
already_handled = np.full((points_arr.shape[0], points_arr.shape[0]), False)
np.fill_diagonal(already_handled, True)  # Ignore main diag for distances initially (dist is 0 there)

print(f"initialized bool mask array of shape {already_handled.shape}")
print("\n", already_handled)

# List of sets (circuits are sets)
circuits = []
connection_count = 1

# Connect closest pair 1000 times
while connection_count <= 1000:

    # Find closest pair in distances matrix (ignore already handled points)
    masked_eucl_distances = np.ma.array(eucl_distances, mask=already_handled)
    min_distance_id = np.argmin(masked_eucl_distances)
    min_distance_id = np.unravel_index(min_distance_id, masked_eucl_distances.shape)
    x, y = int(min_distance_id[0]), int(min_distance_id[1])
    print(f"Got id pair ({x}, {y})")

    # Ignore handled ids in future iterations (add to bool mask)
    already_handled[x, y] = True
    already_handled[y, x] = True

    # Find circuit ids of x and y if they exist in any circuit already
    x_circuit_id, y_circuit_id = None, None
    for i, circuit in enumerate(circuits):
        if x in circuit:
            x_circuit_id = i
        if y in circuit:
            y_circuit_id = i

    # Case: Neither id is known/in a circuit: Create new set/circuit & add to list
    if x_circuit_id is None and y_circuit_id is None:
        circuits.append({x, y})
        #print(f"Created new circuit: {circuits[-1]}")
    
    # Case: Both ids are known already
    elif x_circuit_id is not None and y_circuit_id is not None:
        
        # Case: Both known & in different circuits -> Merge them (set union)
        if x_circuit_id != y_circuit_id:
            circuits[x_circuit_id].update(circuits[y_circuit_id])
            del circuits[y_circuit_id]
    
    # Case: First id is known only: Add second id to set
    elif x_circuit_id is not None:
        # x in circuit, y is new - add y
        circuits[x_circuit_id].add(y)
        #print(f"Added {y} to circuit: {circuits[x_circuit_id]}")

    # Case: Second id is known only: Add first id to set
    else:
        circuits[y_circuit_id].add(x)
        #print(f"Added {x} to circuit: {circuits[y_circuit_id]}")

    connection_count += 1

# Sort "circuits" in-place by len
circuits.sort(key=lambda x: len(x), reverse=True)
top_3 = [len(circuit) for circuit in circuits][:3]
prod_len_top_3 = prod(top_3)
print("\nPart 1:", prod_len_top_3)