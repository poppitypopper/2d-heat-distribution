from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
import copy
import sys

np.set_printoptions(threshold = np.inf)

def process_image(image_path, color_mapping, resolution=(500, 500)):
    
    image = Image.open(image_path).convert("RGB")
    image = image.resize(resolution)  
    pixels = np.array(image)

    height, width = resolution
    processed_array = np.zeros((height, width), dtype=int)

    for rgb, value in color_mapping.items():
        mask = np.all(pixels == np.array(rgb), axis=-1) 
        processed_array[mask] = value

    return processed_array

color_mapping = {
    (0, 108, 234): 0,   
    (255, 255, 255): -1,   
    (0, 0, 0): 1   
}

image_path = "500x500(double border).png"  # Replace with your image path
processed_array = process_image(image_path, color_mapping)

plt.imshow(processed_array)
plt.show()

skeleton_array = processed_array
skeleton_array = copy.deepcopy(processed_array)
for i in range(len(skeleton_array)):
    for j in range(len(skeleton_array[i])):
        if skeleton_array[i][j] == -1: 
            skeleton_array[i][j] = 0
        elif skeleton_array[i][j] == 0:
            skeleton_array[i][j] = 0
        else :
            skeleton_array[i][j] = 1

print(skeleton_array)

plt.imshow(skeleton_array)
plt.show()


def label_loops(grid):
    rows, cols = len(grid), len(grid[0])
    label = 1  # Starting label for the first loop
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
                label += 10  # Increment label for the next loop

    return grid

labelled_skeleton = label_loops(skeleton_array)
plt.imshow(labelled_skeleton)
plt.show()


