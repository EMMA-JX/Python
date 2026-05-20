import os.path
import numpy as np
import torch
from torch.utils.data import Dataset
from datasets import load_dataset
from tqdm import tqdm
from scipy.ndimage import center_of_mass
import scipy.io as sio


class PanNukeDataset(Dataset):
    def __init__(self, dataset_path: str, seq_length: int, folder_name = "fold1", npz_path=None, transform=None):
        self.seq_length = seq_length
        self.transform = transform

        if os.path.exists(npz_path):
            data = np.load(npz_path)
            self.images = data["images"]
            self.masks = data["masks"]
            self.h_maps = data["h_maps"]
            self.v_maps = data["v_maps"]
        else:
            self.images = []
            self.masks = []
            self.h_maps = []
            self.v_maps = []

            dataset = load_dataset("RationAI/PanNuke", cache_dir=dataset_path)
            dataset = dataset[folder_name]

            for index, data in enumerate(tqdm(dataset, desc="Loading data")):
                image = np.array(data["image"])

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

                self.images.append(image)
                self.masks.append(mask.astype(np.uint8))
                self.h_maps.append(h_map)
                self.v_maps.append(v_map)
                sio.savemat(f"./mat/{folder_name}/gt/gt_{index}.mat", {"inst_map": inst_map})

            np.savez_compressed(npz_path,
                                images=np.array(self.images),
                                masks=np.array(self.masks),
                                h_maps=np.array(self.h_maps),
                                v_maps=np.array(self.v_maps))

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        image = self.images[index]
        mask = self.masks[index]
        h_map = self.h_maps[index]
        v_map = self.v_maps[index]

        if self.transform:
            augmented = self.transform["geometry"](image=image, mask=mask, h_map=h_map, v_map=v_map)
            image = augmented["image"]
            mask = augmented["mask"]
            h_map = augmented["h_map"]
            v_map = augmented["v_map"]
            image = self.transform["color"](image=image)["image"]

        image = torch.tensor(np.clip(image, 0, 255).astype(np.uint8).transpose(2, 0, 1))
        mask = torch.tensor(mask).type(torch.int64).unsqueeze(0)
        h_map = torch.tensor(h_map).unsqueeze(0)
        v_map = torch.tensor(v_map).unsqueeze(0)

        return image, mask, h_map, v_map
