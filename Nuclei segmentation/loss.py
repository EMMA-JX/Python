import torch
import torch.nn.functional as F


def xentropy_loss(pred, target, smooth=1e-7, reduction="mean"):
    '''
    :param pred: [N, 2, H, W]
    :param target: [N, 2, H, W]
    '''
    pred = pred / torch.sum(pred, 1, keepdim=True)
    pred = torch.clamp(pred, smooth, 1.0 - smooth)
    loss = -torch.sum(target * torch.log(pred), dim=1)

    if reduction == "mean":
        return loss.mean()
    else:
        return loss.sum()


def dice_loss(pred, target, smooth=1e-5):
    '''
    :param pred: [N, 2, H, W]
    :param target: [N, 2, H, W]
    '''

    intersection = torch.sum(pred * target, dim=(0, 2, 3))  # sum over N, H, W
    l = torch.sum(pred, dim=(0, 2, 3))  # prediction volume per class
    r = torch.sum(target, dim=(0, 2, 3))  # ground truth volume per class

    dice_per_class = (2.0 * intersection + smooth) / (l + r + smooth)
    loss = 1.0 - dice_per_class
    return loss.sum()


def mse_loss(pred, true_hv, focus):
    '''
    :param pred: [N, 2, H, W]
    :param true_hv: [N, 2, H, W]
    '''
    loss = ((pred - true_hv) ** 2).mean()
    return loss


####
def msge_loss(pred, true_hv, focus):
    '''
    :param pred: [N, 2, H, W]
    :param true_hv: [N, 2, H, W]
    :param focus: [N, H, W]
    '''

    def get_sobel_kernel(size):
        """Get sobel kernel with a given size."""
        h_range = torch.arange(-size // 2 + 1, size // 2 + 1, dtype=torch.float32, device="cuda", requires_grad=False)
        v_range = torch.arange(-size // 2 + 1, size // 2 + 1, dtype=torch.float32, device="cuda", requires_grad=False)

        h, v = torch.meshgrid(h_range, v_range, indexing='ij')

        kernel_h = h / (h * h + v * v + 1.0e-15)
        kernel_v = v / (h * h + v * v + 1.0e-15)

        kernel_h = kernel_h.view(1, 1, size, size)
        kernel_v = kernel_v.view(1, 1, size, size)

        return kernel_h, kernel_v

    ####
    def get_gradient_hv(hv):
        """For calculating gradient."""
        kernel_h, kernel_v = get_sobel_kernel(5)  # 5x5 kernel

        h_ch = hv[:, 0:1, :, :]  # Horizontal → channel 0
        v_ch = hv[:, 1:2, :, :]  # Vertical   → channel 1

        h_dh = F.conv2d(h_ch, kernel_h, padding=2)
        v_dv = F.conv2d(v_ch, kernel_v, padding=2)

        return torch.cat([h_dh, v_dv], dim=1)  # [N, 2, H, W]

    true_grad = get_gradient_hv(true_hv)
    pred_grad = get_gradient_hv(pred)

    focus = focus.unsqueeze(1).float()
    focus = torch.cat([focus, focus], dim=1)

    loss = pred_grad - true_grad
    loss = focus * (loss * loss)
    # artificial reduce_mean with focused region
    loss = loss.sum() / (focus.sum() + 1.0e-8)
    return loss


def loss_fn(model_type, pred, target, focus=None):
    if model_type == "mask":
        xentropy = xentropy_loss(pred, target)
        dice = dice_loss(pred, target)
        return xentropy + dice
    elif model_type == "hv":
        mse = mse_loss(pred, target, focus)
        msge = msge_loss(pred, target, focus)
        return mse + msge
