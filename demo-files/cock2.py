from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
import copy
import sys
from matplotlib.animation import FuncAnimation

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

class HeatDiffusion:
    def __init__(self, initial_array, edge_temps, thermal_diffusivity):
        self.temp_array = np.array(initial_array, dtype=float)
        self.edge_temps = edge_temps
        self.alpha = thermal_diffusivity
        self.dx = self.dy = 1
        self.dt = 0.1
        
    def update(self):
        new_temp = np.copy(self.temp_array)
        rows, cols = self.temp_array.shape
        rx = self.alpha * self.dt / (self.dx * self.dx)
        ry = self.alpha * self.dt / (self.dy * self.dy)
        
        if rx + ry > 0.5:
            raise ValueError(f"Simulation unstable. Current rx+ry={rx+ry}, should be ≤ 0.5")
        
        for i in range(1, rows-1):
            for j in range(1, cols-1):
                if self.temp_array[i][j] in self.edge_temps:
                    continue
                new_temp[i, j] = self.temp_array[i, j] + \
                    rx * (self.temp_array[i+1, j] - 2*self.temp_array[i, j] + self.temp_array[i-1, j]) + \
                    ry * (self.temp_array[i, j+1] - 2*self.temp_array[i, j] + self.temp_array[i, j-1])
        
        self.temp_array = new_temp
        return self.temp_array

def setup_simulation(image_path, resolution=(500, 500)):
    color_mapping = {
        (0, 108, 234): 0,    # Blue -> Background
        (255, 255, 255): -1, # White -> Gaps
        (0, 0, 0): 1        # Black -> Loops
    }
    
    processed_array = process_image(image_path, color_mapping, resolution)
    skeleton_array = copy.deepcopy(processed_array)
    skeleton_array[skeleton_array <= 0] = 0
    
    labeled_skeleton, num_labels = label(skeleton_array)
    print(f"Number of detected regions: {num_labels}")
    
    # Show the labeled regions
    plt.figure(figsize=(10, 5))
    plt.subplot(121)
    plt.imshow(skeleton_array, cmap='gray')
    plt.title("Skeleton Array")
    plt.subplot(122)
    plt.imshow(labeled_skeleton, cmap='tab20')
    plt.title(f"Labeled Regions ({num_labels} regions)")
    plt.colorbar()
    plt.show()
    
    edge_temperatures = [100, 200, 300]
    if num_labels > len(edge_temperatures):
        print(f"Warning: More regions ({num_labels}) than temperatures ({len(edge_temperatures)})")
        print("Generating additional temperatures...")
        edge_temperatures = np.linspace(100, 300, num_labels).tolist()
    
    surface_temp = 25
    bulk_array = np.full(resolution, surface_temp, dtype=float)
    edge_array = np.zeros(resolution, dtype=float)
    
    for i in range(1, num_labels + 1):
        edge_array[labeled_skeleton == i] = edge_temperatures[i-1]
    
    initial_temps = np.where(edge_array > 0, edge_array, bulk_array)
    return initial_temps, edge_temperatures

def animate_heat_diffusion(image_path):
    initial_temps, edge_temps = setup_simulation(image_path)
    # Increased thermal diffusivity for faster heat spread
    sim = HeatDiffusion(initial_temps, edge_temps, thermal_diffusivity=1.32e-4)  
    
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(sim.temp_array, cmap='hot')
    plt.colorbar(im)
    
    def update(frame):
        # Reduced steps per frame
        for _ in range(20):  # Changed from 100 to 20
            sim.update()
        im.set_array(sim.temp_array)
        ax.set_title(f'Time step: {frame}')
        return [im]
    
    # Reduced number of frames and increased interval
    anim = FuncAnimation(fig, update, frames=50, interval=100, blit=True)  # Changed from 200 to 50 frames
    anim.save('heat_diffusion.gif', writer='pillow')
    plt.show()

if __name__ == "__main__":
    animate_heat_diffusion("500x500(double border).png")