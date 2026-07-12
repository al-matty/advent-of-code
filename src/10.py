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
    additionally create a limiting shape from input points (connected in order)
    main_shape              <- bool mask: True = inside or on polygon boundary
    build_shape()           <- trace polygon edges, fill interior between boundaries
    is_within_main_shape()  <- True if ALL tiles in rectangle are within main_shape

    to not get stuck: pre-generate all rectangles, sort by area descending
    all_rects               <- list of (area, rect) tuples, sorted largest first
    process largest first, skip smaller ones once valid rectangle found
    early exit when remaining rectangles are all smaller than current best
"""

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

    # Make a copy to avoid mutating original list
    points = points.copy()

    # Initial full grid: all False
    bool_mask = np.full((grid_shape_x, grid_shape_y), False)
    print("\nbool_mask before:")
    print(bool_mask)
    
    points.append(points[0])
    print("\npoints after wrap:")
    print(points)

    points_extended = []

    # Trace lines between consecutive points (they always share row OR col)
    for i in range(len(points) - 1):  # -1 because we already appended wrap
        p1 = points[i]
        p2 = points[i + 1]
        print(f"\nTracing line from {p1} to {p2}")

        # Case: Same row -> fill columns between them
        if p1[0] == p2[0]:
            row = p1[0]
            col_start = min(p1[1], p2[1])
            col_end = max(p1[1], p2[1])
            print(f"Same row {row}, filling cols {col_start} to {col_end}")

            for col in range(col_start, col_end + 1):
                new_point = (row, col)
                points_extended.append(new_point)
                print(f"  Added {new_point}")

        # Case: Same col -> fill rows between them
        else:
            col = p1[1]
            row_start = min(p1[0], p2[0])
            row_end = max(p1[0], p2[0])
            print(f"Same col {col}, filling rows {row_start} to {row_end}")

            for row in range(row_start, row_end + 1):
                new_point = (row, col)
                points_extended.append(new_point)
                print(f"  Added {new_point}")

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
    """Part 2 only: True if ALL tiles in rectangle are within main_shape."""

    # Initial check if any corner is outside
    for coord in rect_coords:
        if not main_shape[coord]:
            return False

    # Full check only if corners pass
    rows = [coord[0] for coord in rect_coords]
    cols = [coord[1] for coord in rect_coords]
    rect_region = main_shape[min(rows):max(rows)+1, min(cols):max(cols)+1]
    return rect_region.all()


# Convert points to (x, y) tuples (x and y are reversed in AoC data)
all_points = [(int(x), int(y)) for y, x in points_arr]

print("\nall_points:")
[print(p) for p in all_points]

# If part 2: Additionally build outer shape as bool mask
if part == 2:
    main_shape = build_shape(all_points, is_point.shape[0], is_point.shape[1])

# Pre-generate all unique rectangle candidates with their areas
print("Generating all rectangle candidates...")
all_rects = []
seen_rectangles = set()

for point in all_points:
    for other_point in all_points:
        # Skip if same row or same col (need diagonal)
        if other_point[0] == point[0] or other_point[1] == point[1]:
            continue

        # Build rectangle
        rect = [point, (point[0], other_point[1]), other_point, (other_point[0], point[1])]

        # Check if already seen
        corners = [tuple(c) for c in rect]
        corners.sort()
        rect_key = tuple(corners)
        if rect_key in seen_rectangles:
            continue
        seen_rectangles.add(rect_key)

        # Store with area
        area = get_area(rect)
        all_rects.append((area, rect))

print(f"Generated {len(all_rects)} unique rectangles")

# Sort by area descending (largest first)
all_rects.sort(reverse=True)

# Process largest first - can stop early once we find a valid one
largest_area = 0
for i, (area, rect) in enumerate(all_rects):
    # Skip if smaller than current best
    if area <= largest_area:
        print(f"Remaining {len(all_rects) - i} rectangles are smaller, done!")
        break

    # Check if valid (part 2)
    if part == 2 and not is_within_main_shape(rect, main_shape):
        continue

    # Found valid rectangle larger than current best
    largest_area = area
    print(f"New largest area: {largest_area}")

print(f"\nPart {part} largest_area:", largest_area)


# Answer too high:  4653414735
# Answer too low:   336022830