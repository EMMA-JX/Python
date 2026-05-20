import os
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP
from torch import optim
from tools import create_dataloaders, check_result
from Model import Net
from tqdm import tqdm
from loss import loss_fn
import torch.nn.functional as F

dataset_path = "./PanNuke"
plt_output_path = "./results/plt_output"
pth_output_path = "./results/pth_output"
weights_pth = "./results/pth_output"
folder_name = "fold1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"
batch_size = 10
epoch_size = 1000
save_plt = True
save_pth = True


def setup_ddp(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    dist.init_process_group("nccl", rank=rank, world_size=world_size)


def cleanup_ddp():
    if dist.is_initialized():
        dist.destroy_process_group()


def train_loop(rank, world_size):
    setup_ddp(rank, world_size)

    torch.cuda.set_device(rank)
    device = torch.device(f"cuda:{rank}")

    dataloader, train_loader, val_loader, test_loader = create_dataloaders(
        dataset_path=dataset_path,
        seq_length=2,
        batch_size=batch_size,
        npz_path="sampled_data.npz",
        ddp=True,
        rank=rank,
        world_size=world_size,
        folder_name=folder_name
    )

    model_mask = Net(model_type="mask", num_classes=2).to(device)
    model_hv = Net(model_type="hv", num_classes=2).to(device)

    model_mask = DDP(model_mask, device_ids=[rank])
    model_hv = DDP(model_hv, device_ids=[rank])
    models = {"mask": model_mask, "hv": model_hv}
    if weights_pth is not None:
        models["mask"].load_state_dict(torch.load(f"{weights_pth}/mask/mask_epoch_992.pth", weights_only=True))
        models["hv"].load_state_dict(torch.load(f"{weights_pth}/hv/hv_epoch_1.pth", weights_only=True))

    optimizers = {
        "mask": optim.Adam(model_mask.parameters(), lr=1e-4, betas=(0.9, 0.999)),
        "hv": optim.Adam(model_hv.parameters(), lr=1e-4, betas=(0.9, 0.999)),
    }

    min_mask_pred_loss = 1000
    min_hv_pred_loss = 1000

    for epoch in range(1, epoch_size + 1):

        train_loader.sampler.set_epoch(epoch)

        for model in models.values():
            model.train()

        train_mask_pred_loss = 0.0
        train_hv_pred_loss = 0.0

        for images, masks, h_maps, v_maps in tqdm(train_loader, desc=f"Rank {rank} Training Epoch {epoch}",
                                                  disable=(rank != 0)):
            images = images.to(device)
            masks = masks.to(device)
            h_maps = h_maps.to(device)
            v_maps = v_maps.to(device)

            masks_onehot = F.one_hot(masks.squeeze(1), num_classes=2).permute(0, 3, 1, 2).float().to(device)

            mask_pred_outputs = models["mask"](images)
            mask_pred_loss = loss_fn("mask", mask_pred_outputs, masks_onehot)

            hv_pred_outputs = models["hv"](images)
            hv_pred_loss = loss_fn("hv", hv_pred_outputs, torch.cat([h_maps, v_maps], dim=1), masks_onehot[:, 1])

            train_mask_pred_loss += mask_pred_loss.item()
            train_hv_pred_loss += hv_pred_loss.item()

            optimizers["mask"].zero_grad()
            mask_pred_loss.backward()
            optimizers["mask"].step()

            optimizers["hv"].zero_grad()
            hv_pred_loss.backward()
            optimizers["hv"].step()

        avg_train_mask_pred_loss = train_mask_pred_loss / len(train_loader)
        avg_train_hv_pred_loss = train_hv_pred_loss / len(train_loader)

        if rank == 0:
            print(
                f"Epoch {epoch}/{epoch_size} - Training Mask Prediction Loss: {avg_train_mask_pred_loss:.4f} - Training HV Prediction Loss: {avg_train_hv_pred_loss:.4f}")

        for model in models.values():
            model.eval()

        valid_mask_pred_loss = 0.0
        valid_hv_pred_loss = 0.0

        image_list = []
        mask_list = []
        h_map_list = []
        v_map_list = []

        mask_output_list = []
        hv_pred_output_list = []

        with torch.no_grad():
            for images, masks, h_maps, v_maps in tqdm(val_loader, desc=f"Rank {rank} Validation", disable=(rank != 0)):
                images = images.to(device)
                masks = masks.to(device)
                h_maps = h_maps.to(device)
                v_maps = v_maps.to(device)

                masks_onehot = F.one_hot(masks.squeeze(1), num_classes=2).permute(0, 3, 1, 2).float().to(device)

                mask_pred_outputs = models["mask"](images)
                mask_pred_loss = loss_fn("mask", mask_pred_outputs, masks_onehot)

                hv_pred_outputs = models["hv"](images)
                hv_pred_loss = loss_fn("hv", hv_pred_outputs, torch.cat([h_maps, v_maps], dim=1), masks_onehot[:, 1])

                valid_mask_pred_loss += mask_pred_loss.item()
                valid_hv_pred_loss += hv_pred_loss.item()

                if rank == 0:
                    image_list.extend(images.cpu())
                    mask_list.extend(masks.cpu())
                    mask_output_list.extend(mask_pred_outputs.cpu())
                    h_map_list.extend(h_maps.cpu())
                    v_map_list.extend(v_maps.cpu())
                    hv_pred_output_list.extend(hv_pred_outputs.cpu())

        valid_mask_tensor = torch.tensor(valid_mask_pred_loss, device=device)
        valid_hv_tensor = torch.tensor(valid_hv_pred_loss, device=device)

        dist.all_reduce(valid_mask_tensor, op=dist.ReduceOp.SUM)
        dist.all_reduce(valid_hv_tensor, op=dist.ReduceOp.SUM)

        avg_valid_mask_pred_loss = valid_mask_tensor.item() / (len(val_loader) * world_size)
        avg_valid_hv_pred_loss = valid_hv_tensor.item() / (len(val_loader) * world_size)

        if rank == 0:
            print(f"Epoch {epoch}/{epoch_size} - Validation Mask Prediction Loss: {avg_valid_mask_pred_loss:.4f} - "
                  f"Validation HV Prediction Loss: {avg_valid_hv_pred_loss:.4f}")

        if rank == 0 and (min_mask_pred_loss > avg_valid_mask_pred_loss or min_hv_pred_loss > avg_valid_hv_pred_loss):
            check_list = {"mask": min_mask_pred_loss > avg_valid_mask_pred_loss,
                          "hv": min_hv_pred_loss > avg_valid_hv_pred_loss}
            check_result(models, image_list, mask_list, mask_output_list, h_map_list, v_map_list, hv_pred_output_list,
                         epoch, save_plt, save_pth, check_list)
            min_mask_pred_loss = avg_valid_mask_pred_loss if min_mask_pred_loss > avg_valid_mask_pred_loss else min_mask_pred_loss
            min_hv_pred_loss = avg_valid_hv_pred_loss if min_hv_pred_loss > avg_valid_hv_pred_loss else min_hv_pred_loss

    print(f"Min mask pred loss: {min_mask_pred_loss}")
    print(f"Min hv pred loss: {min_hv_pred_loss}")

    cleanup_ddp()


if __name__ == '__main__':
    world_size = torch.cuda.device_count()
    mp.spawn(train_loop, args=(world_size,), nprocs=world_size, join=True)
