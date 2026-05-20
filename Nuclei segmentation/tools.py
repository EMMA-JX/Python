import json
import os
import scipy.io as sio
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, random_split
from torch.utils.data.distributed import DistributedSampler
from tqdm import tqdm
from dataset import PanNukeDataset
import matplotlib.pyplot as plt
import albumentations as A
import cv2
from scipy.ndimage import measurements
from scipy.ndimage.morphology import binary_fill_holes
from skimage.segmentation import watershed
from scipy import ndimage
from metrics import (
    get_dice_1,
    get_fast_aji,
    get_fast_aji_plus,
    get_fast_pq,
    remap_label
)

torch.set_printoptions(precision=16)


def create_dataloaders(dataset_path, seq_length, batch_size, npz_path, ddp=False, rank=0, world_size=1,
                       folder_name="fold1"):
    preprocess = {
        "geometry": A.Compose([
            A.Affine(
                scale=(0.8, 1.2),
                translate_percent={"x": (-0.01, 0.01), "y": (-0.01, 0.01)},
                shear=(-5, 5),
                rotate=(-179, 179),
                interpolation=0,
                border_mode=0,
                p=0.5),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.5)
        ], additional_targets={'mask': 'mask', "h_map": "mask", "v_map": "mask"}),

        "color": A.Compose([
            A.OneOf([
                A.GaussianBlur(blur_limit=(1, 3), p=0.5),
                A.MedianBlur(blur_limit=3, p=0.5),
                A.GaussNoise(std_range=(np.sqrt(10 / 255), np.sqrt(30 / 255)), mean_range=(0.0, 0.0), p=0.5),
            ], p=0.5),
            A.ColorJitter(
                brightness=0.2,
                contrast=0.25,
                saturation=0.2,
                hue=0.03,
                p=0.5)
        ])
    }

    full_dataset = PanNukeDataset(dataset_path, seq_length, folder_name, npz_path=npz_path, transform=preprocess)
    total_len = len(full_dataset)
    train_len = int(0.8 * total_len)
    val_len = int(0.2 * total_len)
    test_len = total_len - train_len - val_len

    train_data, val_data, test_data = random_split(full_dataset, [train_len, val_len, test_len])

    if ddp:
        train_sampler = DistributedSampler(train_data, num_replicas=world_size, rank=rank, shuffle=True)
        val_sampler = DistributedSampler(val_data, num_replicas=world_size, rank=rank, shuffle=False)
        test_sampler = DistributedSampler(test_data, num_replicas=world_size, rank=rank, shuffle=False)
    else:
        train_sampler = None
        val_sampler = None
        test_sampler = None

    train_dataloader = DataLoader(train_data, batch_size=batch_size, sampler=train_sampler,
                                  shuffle=(train_sampler is None), num_workers=4, pin_memory=True,
                                  persistent_workers=True)
    valid_dataloader = DataLoader(val_data, batch_size=batch_size, sampler=val_sampler,
                                  shuffle=False, num_workers=4, pin_memory=True, persistent_workers=True)
    test_dataloader = DataLoader(test_data, batch_size=batch_size, sampler=test_sampler,
                                 shuffle=False, num_workers=4, pin_memory=True, persistent_workers=True)

    # 可选：返回完整 dataset 的普通 dataloader（不建议在 DDP 中用）
    # dataloader = DataLoader(full_dataset, batch_size=batch_size, shuffle=False)
    dataloader = None

    return dataloader, train_dataloader, valid_dataloader, test_dataloader


def check_result(models, images, masks, mask_pred_outputs, h_maps, v_maps, hv_pred_outputs, epoch, save_plt, save_pth,
                 check_list):
    if check_list is not None:
        if check_list["mask"]:
            plt_mask(images, masks, mask_pred_outputs, epoch, save_plt)
            if save_pth:
                os.makedirs("./results/pth_output/mask/", exist_ok=True)
                torch.save(models["mask"].state_dict(), f"./results/pth_output/mask/mask_epoch_{epoch}.pth")
        if check_list["hv"]:
            plt_hv(h_maps, v_maps, hv_pred_outputs, epoch, save_plt)
            if save_pth:
                os.makedirs("./results/pth_output/hv/", exist_ok=True)
                torch.save(models["hv"].state_dict(), f"./results/pth_output/hv/hv_epoch_{epoch}.pth")


def plt_mask(images, masks, outputs, epoch, save_plt):
    idx = 0
    sample_images = images[idx].cpu().numpy()
    sample_masks = masks[idx].cpu().numpy()
    predicted_masks = outputs[idx][1].cpu().numpy()

    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].imshow(sample_images.transpose(1, 2, 0))
    ax[0].set_title('Input Image')
    ax[0].axis('off')

    ax[1].imshow(sample_masks.squeeze(), cmap='gray')
    ax[1].set_title('Ground Truth')
    ax[1].axis('off')

    ax[2].imshow(predicted_masks.squeeze(), cmap='gray')
    ax[2].set_title('Predicted Mask')
    ax[2].axis('off')

    plt.suptitle(f'Epoch {epoch}')
    if save_plt:
        os.makedirs("./results/plt_output/mask/", exist_ok=True)
        plt.savefig(f"./results/plt_output/mask/Epoch_{epoch}.png")
    else:
        plt.show()


def plt_hv(h_maps, v_maps, outputs, epoch, save_plt):
    idx = 0
    gt_h = h_maps[idx].squeeze().detach().cpu()
    gt_v = v_maps[idx].squeeze().detach().cpu()
    pred_h = outputs[idx][0].squeeze().detach().cpu()
    pred_v = outputs[idx][1].squeeze().detach().cpu()
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    im0 = axs[0, 0].imshow(gt_h, cmap='coolwarm', vmin=-1, vmax=1)
    axs[0, 0].set_title('GT Horizontal')

    im1 = axs[0, 1].imshow(gt_v, cmap='coolwarm', vmin=-1, vmax=1)
    axs[0, 1].set_title('GT Vertical')

    im2 = axs[1, 0].imshow(pred_h, cmap='coolwarm', vmin=-1, vmax=1)
    axs[1, 0].set_title('Pred Horizontal')

    im3 = axs[1, 1].imshow(pred_v, cmap='coolwarm', vmin=-1, vmax=1)
    axs[1, 1].set_title('Pred Vertical')

    # 添加 colorbar（共享）
    fig.colorbar(im3, ax=axs, orientation='vertical', fraction=0.02, pad=0.04)

    plt.suptitle(f"Epoch {epoch}")
    if save_plt:
        os.makedirs("./results/plt_output/hv/", exist_ok=True)
        plt.savefig(f"./results/plt_output/hv/Epoch_{epoch}.png")
    else:
        plt.show()


def get_bounding_box(img):
    """Get bounding box coordinate information."""
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    # due to python indexing, need to add 1 to max
    # else accessing will be 1px in the box, not out
    rmax += 1
    cmax += 1
    return [rmin, rmax, cmin, cmax]


def process_ground_truth(inst_mask):
    inst_info_dict = {}

    inst_id_list = np.unique(inst_mask)
    inst_id_list = inst_id_list[inst_id_list != 0]

    for inst_id in inst_id_list:
        inst_map = inst_mask == inst_id
        rmin, rmax, cmin, cmax = get_bounding_box(inst_map)
        inst_bbox = np.array([[rmin, cmin], [rmax, cmax]])

        inst_map_crop = inst_map[rmin:rmax, cmin:cmax].astype(np.uint8)

        inst_moment = cv2.moments(inst_map_crop)
        contours = cv2.findContours(inst_map_crop, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        inst_contour = np.squeeze(contours[0][0].astype("int32"))

        if inst_contour.shape[0] < 3 or len(inst_contour.shape) != 2:
            continue

        inst_centroid = [
            inst_moment["m10"] / (inst_moment["m00"] + 1e-6),
            inst_moment["m01"] / (inst_moment["m00"] + 1e-6),
        ]
        inst_centroid = np.array(inst_centroid)

        inst_contour[:, 0] += cmin
        inst_contour[:, 1] += rmin
        inst_centroid[0] += cmin
        inst_centroid[1] += rmin

        inst_info_dict[inst_id] = {
            "bbox": inst_bbox,
            "centroid": inst_centroid,
            "contour": inst_contour,
            "type": None,
            "type_prob": None
        }

    return inst_mask, inst_info_dict


def remove_small_objects(pred, min_size=64, connectivity=1):
    """Remove connected components smaller than the specified size.

    This function is taken from skimage.morphology.remove_small_objects, but the warning
    is removed when a single label is provided.

    Args:
        pred: input labelled array
        min_size: minimum size of instance in output array
        connectivity: The connectivity defining the neighborhood of a pixel.

    Returns:
        out: output array with instances removed under min_size

    """
    out = pred

    if min_size == 0:  # shortcut for efficiency
        return out

    if out.dtype == bool:
        selem = ndimage.generate_binary_structure(pred.ndim, connectivity)
        ccs = np.zeros_like(pred, dtype=np.int32)
        ndimage.label(pred, selem, output=ccs)
    else:
        ccs = out

    try:
        component_sizes = np.bincount(ccs.ravel())
    except ValueError:
        raise ValueError(
            "Negative value labels are not supported. Try "
            "relabeling the input with `scipy.ndimage.label` or "
            "`skimage.morphology.label`."
        )

    too_small = component_sizes < min_size
    too_small_mask = too_small[ccs]
    out[too_small_mask] = 0

    return out


def proc_np_hv(pred):
    """Process Nuclei Prediction with XY Coordinate Map.

    Args:
        pred: prediction output, assuming
              channel 0 contain probability map of nuclei
              channel 1 containing the regressed X-map
              channel 2 containing the regressed Y-map

    """
    pred = np.array(pred, dtype=np.float32)

    blb_raw = pred[..., 0]
    h_dir_raw = pred[..., 1]
    v_dir_raw = pred[..., 2]

    blb = np.array(blb_raw >= 0.5, dtype=np.int32)

    blb = measurements.label(blb)[0]
    blb = remove_small_objects(blb, min_size=10)
    blb[blb > 0] = 1

    h_dir = cv2.normalize(
        h_dir_raw, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F
    )
    v_dir = cv2.normalize(
        v_dir_raw, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F
    )

    sobelh = cv2.Sobel(h_dir, cv2.CV_64F, 1, 0, ksize=21)
    sobelv = cv2.Sobel(v_dir, cv2.CV_64F, 0, 1, ksize=21)

    sobelh = 1 - (
        cv2.normalize(
            sobelh, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F
        )
    )
    sobelv = 1 - (
        cv2.normalize(
            sobelv, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F
        )
    )

    overall = np.maximum(sobelh, sobelv)
    overall = overall - (1 - blb)
    overall[overall < 0] = 0

    dist = (1.0 - overall) * blb
    ## nuclei values form mountains so inverse to get basins
    dist = -cv2.GaussianBlur(dist, (3, 3), 0)

    overall = np.array(overall >= 0.4, dtype=np.int32)

    marker = blb - overall
    marker[marker < 0] = 0
    marker = binary_fill_holes(marker).astype("uint8")
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    marker = cv2.morphologyEx(marker, cv2.MORPH_OPEN, kernel)
    marker = measurements.label(marker)[0]
    marker = remove_small_objects(marker, min_size=10)

    proced_pred = watershed(dist, markers=marker, mask=blb)

    return proced_pred


def process(pred_map):
    pred_inst = pred_map

    pred_inst = np.squeeze(pred_inst)
    pred_inst = proc_np_hv(pred_inst)

    inst_id_list = np.unique(pred_inst)[1:]  # exlcude background
    inst_info_dict = {}
    for inst_id in inst_id_list:
        inst_map = pred_inst == inst_id
        # TODO: chane format of bbox output
        rmin, rmax, cmin, cmax = get_bounding_box(inst_map)
        inst_bbox = np.array([[rmin, cmin], [rmax, cmax]])
        inst_map = inst_map[
                   inst_bbox[0][0]: inst_bbox[1][0], inst_bbox[0][1]: inst_bbox[1][1]
                   ]
        inst_map = inst_map.astype(np.uint8)
        inst_moment = cv2.moments(inst_map)
        inst_contour = cv2.findContours(
            inst_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        # * opencv protocol format may break
        inst_contour = np.squeeze(inst_contour[0][0].astype("int32"))
        # < 3 points dont make a contour, so skip, likely artifact too
        # as the contours obtained via approximation => too small or sthg
        if inst_contour.shape[0] < 3:
            continue
        if len(inst_contour.shape) != 2:
            continue  # ! check for trickery shape
        inst_centroid = [
            (inst_moment["m10"] / inst_moment["m00"]),
            (inst_moment["m01"] / inst_moment["m00"]),
        ]
        inst_centroid = np.array(inst_centroid)
        inst_contour[:, 0] += inst_bbox[0][1]  # X
        inst_contour[:, 1] += inst_bbox[0][0]  # Y
        inst_centroid[0] += inst_bbox[0][1]  # X
        inst_centroid[1] += inst_bbox[0][0]  # Y
        inst_info_dict[inst_id] = {  # inst_id should start at 1
            "bbox": inst_bbox,
            "centroid": inst_centroid,
            "contour": inst_contour,
            "type_prob": None,
            "type": None,
        }

    return pred_inst, inst_info_dict


def save_inst_info_to_geojson(inst_info_dict, save_path):
    features = []

    for inst_id, inst_data in inst_info_dict.items():
        contour = inst_data["contour"]  # [N, 2], columns are (x, y)

        # GeoJSON expects coordinates in [ [ [x1, y1], ..., [xn, yn], [x1, y1] ] ] format
        polygon = contour.tolist()
        if polygon[0] != polygon[-1]:
            polygon.append(polygon[0])  # close the polygon

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon]
            },
            "properties": {
                "id": int(inst_id),
                "centroid_x": float(inst_data["centroid"][0]),
                "centroid_y": float(inst_data["centroid"][1]),
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(save_path, "w") as f:
        json.dump(geojson, f, indent=2)


def save_inst_info_to_mat(inst_info_dict, save_path):
    inst_map = np.zeros((256, 256), dtype=np.int32)

    for inst_id, inst_data in inst_info_dict.items():
        contour = inst_data["contour"].astype(np.int32)

        if contour.ndim != 2 or contour.shape[0] < 3:
            continue

        contour = contour.reshape((-1, 1, 2))
        cv2.drawContours(inst_map, [contour], -1, int(inst_id), thickness=-1)

    sio.savemat(save_path, {"inst_map": inst_map})


def eval_output(true_paths, pred_paths):
    eval_metrics = [[], [], [], [], [], []]

    for i in tqdm(range(len(true_paths)), desc="Evaluating"):
        true_path = true_paths[i]
        pred_path = pred_paths[i]

        true = sio.loadmat(true_path)["inst_map"].astype("int32")
        pred = sio.loadmat(pred_path)["inst_map"].astype("int32")

        true = remap_label(true, by_size=False)
        pred = remap_label(pred, by_size=False)

        if np.max(true) == 0:
            if np.max(pred) == 0:
                eval_metrics[0].append(1.0)  # dice
                eval_metrics[1].append(1.0)  # aji
                eval_metrics[2].append(1.0)  # dq
                eval_metrics[3].append(1.0)  # sq
                eval_metrics[4].append(1.0)  # pq
                eval_metrics[5].append(1.0)  # aji+
            else:
                # 没有GT但预测了，说明误检
                eval_metrics[0].append(0.0)
                eval_metrics[1].append(0.0)
                eval_metrics[2].append(0.0)
                eval_metrics[3].append(0.0)
                eval_metrics[4].append(0.0)
                eval_metrics[5].append(0.0)
        else:
            pq_info, indexes = get_fast_pq(true, pred, match_iou=0.5)

            eval_metrics[0].append(get_dice_1(true, pred))
            eval_metrics[1].append(get_fast_aji(true, pred))
            eval_metrics[2].append(pq_info[0])  # dq
            eval_metrics[3].append(pq_info[1])  # sq
            eval_metrics[4].append(pq_info[2])  # pq
            eval_metrics[5].append(get_fast_aji_plus(true, pred))

    eval_metrics = np.array(eval_metrics)
    metrics_avg = np.mean(eval_metrics, axis=-1)
    np.set_printoptions(formatter={"float": "{: 0.5f}".format})

    items = ["DICE", "AJI", "DQ", "SQ", "PQ", "AJI+"]
    print(f"Net Metrics: {metrics_avg}")

    df = pd.DataFrame([items, metrics_avg])
    print(df.to_string(index=False, header=False))

    return metrics_avg
