import numpy as np
from datasets import load_dataset
from matplotlib import pyplot as plt
from scipy.ndimage import center_of_mass
import scipy.io as sio

base_path = "./test_image"
folder_name = "fold1"

def plot_image_with_instances(image, instances, gap=10):
    """
    image: PIL.Image RGB
    instances: list of PIL.Image mode '1'
    """
    assert len(instances) == 16, "Must have 16 instances"

    image_np = np.array(image)

    instances_np = [np.array(inst).astype(np.uint8) for inst in instances]
    h, w = instances_np[0].shape
    rows, cols = 4, 4

    canvas_h = rows * h + (rows - 1) * gap
    canvas_w = cols * w + (cols - 1) * gap
    canvas = np.ones((canvas_h, canvas_w), dtype=np.uint8) * 255

    for idx, inst in enumerate(instances_np):
        r = idx // cols
        c = idx % cols
        y = r * (h + gap)
        x = c * (w + gap)
        canvas[y:y + h, x:x + w] = inst * 255

    merged_mask = np.clip(np.sum(instances_np, axis=0), 0, 1).astype(np.uint8) * 255

    plt.imsave(f"{base_path}/original.png", image_np)
    plt.imsave(f"{base_path}/instances_grid.png", canvas, cmap='gray')
    plt.imsave(f"{base_path}/merged_mask.png", merged_mask, cmap='gray')

    mask = np.zeros((256, 256), dtype=np.uint8)
    h_map = np.zeros((256, 256), dtype=np.float32)
    v_map = np.zeros((256, 256), dtype=np.float32)
    inst_map = np.zeros((256, 256), dtype=np.int32)
    current_id = 1

    for instance in data["instances"]:
        instance = np.array(instance).astype(np.uint8)

        if instance.sum() == 0:
            continue

        mask[instance > 0] = 1

        # Center of mass
        cy, cx = center_of_mass(instance)
        cy = int(round(cy))
        cx = int(round(cx))

        y_coords, x_coords = np.meshgrid(np.arange(256), np.arange(256), indexing='ij')
        dx = (x_coords - cx).astype(np.float32)
        dy = (y_coords - cy).astype(np.float32)

        dx[instance == 0] = 0
        dy[instance == 0] = 0

        # Normalize to [-1, 1]
        if np.any(dx < 0):
            dx[dx < 0] /= -np.min(dx[dx < 0])
        if np.any(dx > 0):
            dx[dx > 0] /= np.max(dx[dx > 0])
        if np.any(dy < 0):
            dy[dy < 0] /= -np.min(dy[dy < 0])
        if np.any(dy > 0):
            dy[dy > 0] /= np.max(dy[dy > 0])

        h_map[instance > 0] = dx[instance > 0]
        v_map[instance > 0] = dy[instance > 0]

        inst_map[instance > 0] = current_id
        current_id += 1

    h_map = ((h_map + 1) / 2 * 255).clip(0, 255).astype(np.uint8)
    v_map = ((v_map + 1) / 2 * 255).clip(0, 255).astype(np.uint8)
    plt.imsave(f"{base_path}/h_map.png", h_map, cmap="gray")
    plt.imsave(f"{base_path}/v_map.png", v_map, cmap="gray")
    sio.savemat("true_inst.mat", {"inst_map": inst_map})


if __name__ == '__main__':
    dataset = load_dataset("RationAI/PanNuke", cache_dir="./PanNuke")
    for data in dataset[folder_name]:
        if len(data["instances"]) == 16:
            plot_image_with_instances(data["image"], data["instances"])
            break
