def label_loops(grid):
    rows, cols = len(grid), len(grid[0])
    label = 11  # Starting label for the first loop
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    def flood_fill(r, c, label):
        stack = [(r, c)]
        while stack:
            x, y = stack.pop()
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] == 1:
                grid[x][y] = label
                for dx, dy in directions:
                    stack.append((x + dx, y + dy))

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:  # Found an unvisited loop
                flood_fill(i, j, label)
                label += 1  # Increment label for the next loop

    return grid

# Example usage:
grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
]

labeled_grid = label_loops(grid)
for row in labeled_grid:
    print(row)
