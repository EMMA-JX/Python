from PIL import Image
import numpy as np
from tools import process, save_inst_info_to_geojson, save_inst_info_to_mat, eval_output, check_result
from dataset import PanNukeDataset
from torch.utils.data import DataLoader
import os
import torch
from Model import Net
from tqdm import tqdm
from loss import loss_fn
import torch.nn.functional as F
import cv2
import scipy.io as sio

dataset_path = "./PanNuke"
weights_pth = "./results/pth_output"
folder_name = "fold1"
check_one_image = True
mat_path = "./mat/fold1"

if not os.path.exists(f"{mat_path}/gt"):
    os.makedirs(f"{mat_path}/gt")

if not os.path.exists(f"{mat_path}/pred"):
    os.makedirs(f"{mat_path}/pred")

batch_size = 50
save_plt = False
save_pth = False


def create_dataloader(dataset_path, seq_length, batch_size, npz_path, folder_name="fold1"):
    full_dataset = PanNukeDataset(dataset_path, seq_length, npz_path=npz_path, folder_name = folder_name)

    dataloader = DataLoader(full_dataset, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True,
                            persistent_workers=True)

    return dataloader


def test_single_image(models, image):
    image_list = []
    mask_list = []
    h_map_list = []
    v_map_list = []

    mask_output_list = []
    hv_pred_output_list = []

    for model in models.values():
        model.eval()

    with torch.no_grad():
        image = image.to(device)
        mask_pred_outputs = models["mask"](image)
        hv_pred_outputs = models["hv"](image)

        pred = torch.cat([mask_pred_outputs[:, 1:, :, :], hv_pred_outputs], dim=1).squeeze(0).permute(1, 2,
                                                                                                      0).cpu().numpy()
        pred_inst, pred_inst_info_dict = process(pred)

        save_inst_info_to_geojson(pred_inst_info_dict, "./results/output_instances.geojson")

        save_inst_info_to_mat(pred_inst_info_dict, "pred_inst.mat")

        eval_metrics = eval_output(["true_inst.mat"], ["pred_inst.mat"])

        image_list.extend(images.cpu())
        mask_list.extend(masks.cpu())
        mask_output_list.extend(mask_pred_outputs.cpu())
        h_map_list.extend(h_maps.cpu())
        v_map_list.extend(v_maps.cpu())
        hv_pred_output_list.extend(hv_pred_outputs.cpu())

        check_list = {"mask": True, "hv": True}
        check_result(models, image_list, mask_list, mask_output_list, h_map_list, v_map_list, hv_pred_output_list,
                     0, save_plt, save_pth, check_list)
    return eval_metrics


def test_dataset(models, dataloader):
    for model in models.values():
        model.eval()

    test_mask_pred_loss = 0.0
    test_hv_pred_loss = 0.0

    count = 0

    with torch.no_grad():
        for batch_idx, (images, masks, h_maps, v_maps) in enumerate(tqdm(dataloader, desc=f"Testing")):
            images = images.to(device)
            masks = masks.to(device)
            h_maps = h_maps.to(device)
            v_maps = v_maps.to(device)

            masks_onehot = F.one_hot(masks.squeeze(1), num_classes=2).permute(0, 3, 1, 2).float().to(device)

            mask_pred_outputs = models["mask"](images)
            mask_pred_loss = loss_fn("mask", mask_pred_outputs, masks_onehot)

            hv_pred_outputs = models["hv"](images)
            hv_pred_loss = loss_fn("hv", hv_pred_outputs, torch.cat([h_maps, v_maps], dim=1),
                                   masks_onehot[:, 1].to(device))

            test_mask_pred_loss += mask_pred_loss.item()
            test_hv_pred_loss += hv_pred_loss.item()

            for i in range(images.size(0)):
                img_id = batch_idx * dataloader.batch_size + i

                pred = torch.cat([mask_pred_outputs[i][1:, :, :], hv_pred_outputs[i]], dim=0).permute(1, 2,
                                                                                                      0).cpu().numpy()

                pred_inst, pred_inst_info_dict = process(pred)

                pred_inst_map = np.zeros((256, 256), dtype=np.int32)

                for inst_id, inst_data in pred_inst_info_dict.items():
                    contour = inst_data["contour"].astype(np.int32)

                    if contour.ndim != 2 or contour.shape[0] < 3:
                        continue

                    contour = contour.reshape((-1, 1, 2))
                    cv2.drawContours(pred_inst_map, [contour], -1, int(inst_id), thickness=-1)

                sio.savemat(f"{mat_path}/pred/pred_{img_id}.mat", {"inst_map": pred_inst_map})
                count += 1

    avg_test_mask_pred_loss = test_mask_pred_loss / len(dataloader)
    avg_test_hv_pred_loss = test_hv_pred_loss / len(dataloader)

    print(
        f"Testing Mask Prediction Loss: {avg_test_mask_pred_loss:.4f} - Testing HV Prediction Loss: {avg_test_hv_pred_loss:.4f}")

    eval_metrics = eval_output([f"{mat_path}/gt/gt_{img_id}.mat" for img_id in range(count)],
                               [f"{mat_path}/pred/pred_{img_id}.mat" for img_id in range(count)])
    return eval_metrics


if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    models = {
        "mask": Net(model_type="mask", num_classes=2),
        "hv": Net(model_type="hv", num_classes=2)
    }
    state_dict = torch.load(f"{weights_pth}/mask/mask_epoch_959.pth", weights_only=True)
    new_state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}
    models["mask"].to(device).load_state_dict(new_state_dict)

    state_dict = torch.load(f"{weights_pth}/hv/hv_epoch_911.pth", weights_only=True)
    new_state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}
    models["hv"].to(device).load_state_dict(new_state_dict)

    loss_fn = loss_fn
    if check_one_image:
        base_path = "/data/hongrui/BMI/Sem 2/AMS 691/project/test_image"
        images = torch.tensor(
            np.array(Image.open(f"{base_path}/original.png").convert("RGB")).transpose(2, 0, 1)).unsqueeze(
            0)  # [1, 3, H, W]
        masks = torch.tensor(np.array(Image.open(f"{base_path}/merged_mask.png").convert("L")) / 255.0).unsqueeze(
            0).unsqueeze(0)
        h_maps = torch.tensor(
            np.array(Image.open(f"{base_path}/h_map.png").convert("L")).astype(np.float32) / 255 * 2 - 1).unsqueeze(
            0).unsqueeze(0)
        v_maps = torch.tensor(
            np.array(Image.open(f"{base_path}/v_map.png").convert("L")).astype(np.float32) / 255 * 2 - 1).unsqueeze(
            0).unsqueeze(0)

        eval_metrics = test_single_image(models, images)
    else:
        dataloader = create_dataloader(dataset_path, seq_length=2, batch_size=batch_size, npz_path="sampled_data.npz", folder_name=folder_name)
        eval_metrics = test_dataset(models, dataloader)

    print(f"Net Metrics: {eval_metrics}")
