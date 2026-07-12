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

Plan part 2:
    create a limiting shape by iterating over input list
    create a second bool mask: Anything outside of that shape is False
    limiting_points     <- list of all corner points
    is_within_limits    <- second bool mask
    add this check to loop & leave everything else unchanged?
"""

from sys import exit
import numpy as np

#in_file = "../data/09_input_test.txt"
in_file = "../data/09_input.txt"
part = 2  # 1 or 2

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

    # Find all points diagonal to this one (diag = different row, different col)
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

def build_shape(points, grid_shape_x, grid_shape_y):
    """Part 2 only: Build bool mask that's True for tiles inside the shape formed by points."""
    
    # Initial full grid: all False
    bool_mask = np.full((grid_shape_x, grid_shape_y), False)
    print("\nbool_mask before:")
    print(bool_mask)
    
    points.append(points[0])
    print("\npoints after wrap:")
    print(points)

    # Create 2 lists from x and y coords
    y = [point[1] for point in points]
    y_unique_ordered = list(sorted(set(y)))
    

    points_extended = []

    # Fill down vertically: Iterate over cols & generate points
    for col in y_unique_ordered:
        # Fetch all points with this y value
        points_on_col = [point for point in points if point[1] == col]
        ordered_x = sorted([p[0] for p in points_on_col])  # Get x-values & sort
        print(f"These x vals are on col {col}:", ordered_x)
        
        # Fill gaps by creating points in between for all missing x values
        filled_x = list(range(ordered_x[0], ordered_x[-1]+1))
        print("Filled them:", filled_x)
        new_points = [(x, col) for x in filled_x]
        print("new_points:", new_points)
        points_extended.extend(new_points)

    print("points_extended:", points_extended)
    
    print("")
    
    for p in points_extended:
        print(f"Attempting to set {p} in bool mask")
        bool_mask[p] = True
    print("\nbool_mask after vertical fill-down:")
    print(bool_mask)

    # Fill horizontal gaps: Directly update bool mask in between outermost points
    for i in range(bool_mask.shape[0]):
        print(f"Iterating over row {i}")
        if not any(bool_mask[i]):  # Skip False only rows
            print(f"Skipped row {i}")
            continue
        # Get outermost points
        point_ids = np.where(bool_mask[i])[0]
        min_true = point_ids[0]   # Leftmost point
        max_true = point_ids[-1]  # Rightmost point
        
        print("point_ids", point_ids)
        print("min_True", min_true)
        print("max_True", max_true)

        # Set all fields in between to True
        bool_mask[i,min_true:max_true] = True

    print("\nbool_mask after horizontal gap-fill:")
    print(bool_mask)

    return bool_mask

def is_within_main_shape(rect_coords, main_shape):
    """Part 2 only: True if all rectangle coords are within main_shape."""
    # rect_coords = list of 4 corner coords
    return all(main_shape[coord] for coord in rect_coords)


largest_area = 0
seen_rectangles = set()

# Convert points to (x, y) tuples (x and y are reversed in AoC data)
all_points = [(int(x), int(y)) for y, x in points_arr]

print("\nall_points before func:")
[print(p) for p in all_points]


# If part 2: Additionally build outer shape as bool mask
if part == 2:
    main_shape = build_shape(all_points, is_point.shape[0], is_point.shape[1])

#exit() # TODO: Remove

# Iterate over existing points only (NOT entire grid)
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

    # Part 2: Filter to rectangles within main_shape
    if part == 2:
        new_rectangles = [r for r in new_rectangles if is_within_main_shape(r, main_shape)]
        if new_rectangles == []:
            print("no rectangles within main_shape")
            continue

    # Get largest rectangle area from the new rectangles
    print(f"found {len(new_rectangles)} new rectangles")
    max_area = max(get_area(rect) for rect in new_rectangles)

    # Update largest_area if larger found
    if max_area > largest_area:
        largest_area = max_area
        print(f"\t\t\t\tnew largest area found: {largest_area}")


print("\nPart 1 (largest_area):", largest_area)


# Answer too high: 4653414735