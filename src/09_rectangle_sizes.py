"""
Plan part 1:
    try brute force over all points
    points_arr                  <- create array with all points in data
    all_points                  <- points as list of (x, y) tuples
    get_area([a,b,c,d])         <- return rectangle area using 4 2d coords
    find_diagonal_rectangles()  <- return all possible rects based on point & all other points
    largest_area                <- always has largest seen rectangle area

    iterate over all points
        get all possible rectangles for this point based on other points in data
        discard all known rectangles (in seen_rectangles set = seen before)
        get largest area from the new rectangles
        overwrite largest_area if new val larger than old
        (maybe some extra stopping condition to be safe?)
    output largest area at the end
"""

import numpy as np

#in_file = "../data/09_input_test.txt"
in_file = "../data/09_input.txt"

# Read data
with open(in_file) as content:
    lines = content.read().splitlines()

# Create coordinates array
points = [[int(coord) for coord in line.split(",")] for line in lines]    
points_arr = np.array(points)

# Create bool mask (= full grid): True where a point exists in data
grid_y = points_arr[:,0].max() + 1
grid_x = points_arr[:,1].max() + 1
is_point = np.full((grid_x, grid_y), False)
for y, x in points_arr:  #  <- x and y are reversed in AoC example
    is_point[x, y] = True

print("\npoints_arr:")
print(points_arr)
print(f"\ncreated points grid of shape: ({grid_x}, {grid_y})" )
print(is_point)

def get_area(coords_list):
    """Return INCLUSIVE rectangle area (grid count) from 4 2d coord tuples list"""
    assert len(coords_list) == 4, "4 corner coords needed here"

    # use max & min to not have to order coords
    x_coords = [coord[0] for coord in coords_list]
    y_coords = [coord[1] for coord in coords_list]
    rect_width = max(x_coords) - min(x_coords) + 1  # include "border"
    rect_height = max(y_coords) - min(y_coords) + 1 # include "border"

    return rect_width * rect_height

def find_diagonal_rectangles(point, all_points):
    """
    Return all valid rectangles where point is one corner.
    Finds all diagonal points (different row AND col) from all_points list.
    """
    rectangles = []
    i, j = point

    # Find all points diagonal to this one (different row AND col)
    for other_point in all_points:
        row, col = other_point

        # Skip if same row or same col (need diagonal)
        if row == i or col == j:
            continue

        # Diagonal point -> Build rectangle
        rect = [point, (i, col), (row, col), (row, j)]
        rectangles.append(rect)

    print(f"Found {len(rectangles)} rectangles for {point}")
    return rectangles


largest_area = 0
seen_rectangles = set()

# Convert points to (x, y) tuples (x and y are reversed in AoC data)
all_points = [(x, y) for y, x in points_arr]

# Iterate over existing points only (not entire grid)
for i, point in enumerate(all_points):
    print(f"Iterating over {point}")

    # Find all rectangles with this point as corner
    rectangles = find_diagonal_rectangles(point, all_points)

    # Case: No rectangles: Skip this point
    if rectangles == []:
        print(f"no diagonal points found for {point}")
        continue

    # Filter out already seen rectangles & ignore
    new_rectangles = []
    for rect in rectangles:
        # Make comparable/searchable by sorting the corners
        corners = [tuple(p) for p in rect]
        corners.sort()
        rect_tup = tuple(corners)

        # Skip if already seen
        if rect_tup in seen_rectangles:
            continue
        # Add to known rectangles set
        seen_rectangles.add(rect_tup)
        new_rectangles.append(rect)

    if new_rectangles == []:
        print("these ones have all been seen before")
        continue

    # Get largest rectangle area from the new rectangles
    print(f"found {len(new_rectangles)} new rectangles")
    max_area = max(get_area(rect) for rect in new_rectangles)

    # Update largest_area if larger found
    if max_area > largest_area:
        largest_area = max_area
        print(f"\t\t\t\tnew largest area found: {largest_area}")


print("\nPart 1 (largest_area):", largest_area)