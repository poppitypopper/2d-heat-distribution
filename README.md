# Analysing heat distributions in 2D homogenous materials 
Analysing temperature profiles of complex 2D shapes with defined temperature on the boundaries (Dirichlet boundary conditions) and homogeneous diffusivity ('rate of spread of heat').

## Outline
1) Solving for an interable expression of the temperature at a general point in the surface at arbitrary time
2) Processing a B/W 2D image of a surface for exposed edges and setting boundary conditions
3) Running the algorithm and visualising the transient heat transfer process through a colormap

## Background 

The 2 dimensional heat equation is given as\
\
$$\frac{\partial T}{\partial t} = C \left( \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} \right) $$\
\
Which, when solved with the finite difference method, yield the values of `T = t + 1` at `(i,j)` with relation to `T = t` as\
\
$$T_{(i, j)}^{(t+1)} = T_{(i, j)}^{( t)} + \alpha \frac{\Delta t}{\Delta x^2} \left( T_{(i+1, j)}^ t + T_{(i-1, j)}^ t + T_{(i, j+1)}^ t + T_{(i, j-1)}^ t - 4T_{(i, j)}^ t \right) $$\
\
Which is an iterable formula for us to find values of T at all points of the surface given boundary temperatures.

## Processing the image

Here we take as input a black and white image of a surface and process it, asking the user for the surface temperatures wherever required using a GUI. The restrictions placed on the image are such : 

1) The image should have a solid blue background
2) The edges must be black in color
3) The surface must be white in color

To process this image, we impose a 2D grid of resolution `res` over it and fill in the values `0 = background`, `1 = edge` and `-1 = surface`

![](https://github.com/poppitypopper/2d-heat-distribution/blob/main/demo-files/500x500.png) ![](https://github.com/poppitypopper/2d-heat-distribution/blob/main/demo-files/500x500G.png)

So, we have here a correlation table : 

| Description | RGB Value | Mapped Integer |
| --- | --- | --- |
| Background | 0-108-234 | -1 |
| Surface | 255-255-255 | 1 |
| Edge | 0-0-0 | 0 |

```python3
# Define the color-to-integer mapping
color_mapping = {
    (0, 108, 234): -1,   # B = 0 
    (255, 255, 255): 1,   # S = 1
    (0, 0, 0): 0   # E = -1
}
```
We process the image to be a 2D list using and visualise it : 

```python3
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

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
    (0, 108, 234): 0,   # B = 0 (Red)
    (255, 255, 255): 1,   # S = 1 (Green)
    (0, 0, 0): -1   # E = -1 (Blue)
}

image_path = "500x500.png"  # Replace with your image path
processed_array = process_image(image_path, color_mapping)


print("Processed 2D List:")
print(processed_array)
plt.imshow(processed_array)
plt.show()
```

There is a puzzle to solve now, which is to find all the edges of the image. We assume that the image has simple geometry like this, with no topological outliers, and then, the problem becomes to find the connected components of the mapped integer and then label them according to their size. Visually, it would look something like this

![](https://github.com/poppitypopper/2d-heat-distribution/blob/main/demo-files/500x500edgemapped.png)

We achieve this by using a search algorithm (BFS, in this case). To start, we edit the array so that only the edges survive

```python3
import copy
skeleton_array = copy.deepcopy(processed_array)
for i in range(len(skeleton_array)):
    for j in range(len(skeleton_array[i])):
        if skeleton_array[i][j] == -1: 
            skeleton_array[i][j] = -5
        elif skeleton_array[i][j] == 0:
            skeleton_array[i][j] = -5
```

And then we utilise a fill-algorithm to find out the connected components.

```python3
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
```

![](https://github.com/poppitypopper/2d-heat-distribution/blob/main/demo-files/skeleton-marked.png) ![](https://github.com/poppitypopper/2d-heat-distribution/blob/main/demo-files/500x500-skeleton-edges.png)

Another, more efficient solution to this problem is to use `scipy.ndimage`.

```python3
# Label loops using scipy.ndimage.label
labeled_skeleton, num_labels = label(skeleton_array)

# Visualize labeled skeleton
plt.imshow(labeled_skeleton, cmap="tab20")
plt.title(f"Labeled Skeleton (Number of Loops: {num_labels})")
plt.colorbar()
plt.show()
```

Now, we add our skeleton image to the bulk image and set temperatures after visualisation. 








