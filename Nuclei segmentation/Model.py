from collections import OrderedDict

import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision.models import ResNet50_Weights



# mask prediction
class Net(nn.Module):
    def __init__(self, model_type, num_classes=1):
        super(Net, self).__init__()
        self.model_type = model_type
        self.num_classes = num_classes

        backbone = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        self.encoder_layers = list(backbone.children())[:-2]

        self.conv1 = nn.Sequential(*self.encoder_layers[:3])  # Conv1

        self.enc1 = nn.Sequential(
            self.encoder_layers[3],
            nn.BatchNorm2d(64, eps=1e-5),
            nn.ReLU(inplace=True),
            self.encoder_layers[4]  # Conv2_x
        )
        self.enc2 = nn.Sequential(
            nn.BatchNorm2d(256, eps=1e-5),
            nn.ReLU(inplace=True),
            self.encoder_layers[5]  # Conv3_x
        )
        self.enc3 = nn.Sequential(
            nn.BatchNorm2d(512, eps=1e-5),
            nn.ReLU(inplace=True),
            self.encoder_layers[6]  # Conv4_x
        )
        self.enc4 = nn.Sequential(
            nn.BatchNorm2d(1024, eps=1e-5),
            nn.ReLU(inplace=True),
            self.encoder_layers[7]  # Conv5_x
        )

        self.bottleneck = nn.Conv2d(2048, 1024, kernel_size=1, bias=False)

        self.dec4 = nn.Sequential(
            # nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        )

        self.dec3 = nn.Sequential(
            nn.Conv2d(1024, 256, kernel_size=5, padding=2, bias=False),

            DenseBlock(256, 8),

            nn.Conv2d(512, 512, kernel_size=1, bias=False),

            nn.Dropout(0.8)
        )

        self.dec2 = nn.Sequential(
            nn.Conv2d(512, 128, kernel_size=5, padding=2, bias=False),

            DenseBlock(128, 4),

            nn.Conv2d(256, 256, kernel_size=1, bias=False),

            nn.Dropout(0.8)
        )

        self.dec1 = nn.Sequential(
            nn.Conv2d(256, 64, kernel_size=5, padding=2, bias=False),

            DenseBlock(64, 2),

            nn.Conv2d(128, 128, kernel_size=1, bias=False),
        )

        self.dec0 = nn.Sequential(
            nn.Conv2d(128, 32, kernel_size=5, padding=2, bias=False),

            DenseBlock(32, 1),

            nn.Conv2d(64, 64, kernel_size=1, bias=False),
        )

        self.final_conv = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=5, padding=2, bias=False),
            nn.BatchNorm2d(64, eps=1e-5),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, num_classes, kernel_size=1),
        )

        self.upsample2x = UpSample2x()

    def forward(self, image, freeze=False):
        input = image / 255.0

        e1 = self.conv1(input)  # (256, 256) -> (128, 128) -> (64, 64)
        with torch.set_grad_enabled(not freeze):
            e2 = self.enc1(e1)  # (64, 64) -> (64, 64)
            e3 = self.enc2(e2)  # (64, 64) -> (32, 32)
            e4 = self.enc3(e3)  # (32, 32) -> (16, 16)
            bottleneck_input = self.enc4(e4)  # (16, 16) -> (8, 8)

        # Bottleneck
        bottleneck_output = self.bottleneck(bottleneck_input)  # (8, 8) -> (8, 8)

        # Decoder (Upsampling)
        d4 = self.dec4(bottleneck_output)  # (8, 8) -> (16, 16)
        d4 = self.upsample2x(d4)

        cat4 = d4 + e4
        d3 = self.dec3(cat4)  # (16, 16) -> (32, 32)
        d3 = self.upsample2x(d3)

        cat3 = d3 + e3
        d2 = self.dec2(cat3)  # (32, 32) -> (64, 64)
        d2 = self.upsample2x(d2)

        cat2 = d2 + e2
        d1 = self.dec1(cat2)  # (64, 64) -> (128, 128)
        d1 = self.upsample2x(d1)

        # cat1 = d1 + e1
        d0 = self.dec0(d1)
        d0 = self.upsample2x(d0)

        output = self.final_conv(d0)  # (128, 128) -> (256, 256)


        if self.model_type == "mask":
            output = torch.softmax(output, dim=1)
        else:
            output = output

        return output


class UpSample2x(nn.Module):
    def __init__(self):
        super(UpSample2x, self).__init__()
        # correct way to create constant within module
        self.register_buffer(
            "unpool_mat", torch.from_numpy(np.ones((2, 2), dtype="float32"))
        )
        self.unpool_mat.unsqueeze(0)

    def forward(self, x):
        input_shape = list(x.shape)
        # unsqueeze is expand_dims equivalent
        # permute is transpose equivalent
        # view is reshape equivalent
        x = x.unsqueeze(-1)  # bchwx1
        mat = self.unpool_mat.unsqueeze(0)  # 1xshxsw
        ret = torch.tensordot(x, mat, dims=1)  # bxcxhxwxshxsw
        ret = ret.permute(0, 1, 2, 4, 3, 5)
        ret = ret.reshape((-1, input_shape[1], input_shape[2] * 2, input_shape[3] * 2))
        return ret


class DenseBlock(nn.Module):
    def __init__(self, in_ch, unit_count):
        super(DenseBlock, self).__init__()

        self.nr_unit = unit_count

        unit_in_ch = in_ch
        self.units = nn.ModuleList()
        for idx in range(unit_count):
            self.units.append(
                nn.Sequential(
                    nn.BatchNorm2d(unit_in_ch, eps=1e-5),
                    nn.ReLU(inplace=True),
                    nn.Conv2d(unit_in_ch, 128, kernel_size=1, bias=False),

                    nn.BatchNorm2d(128, eps=1e-5),
                    nn.ReLU(inplace=True),
                    nn.Conv2d(128, 32, kernel_size=5, padding=2, bias=False, groups=4),
                )
            )
            unit_in_ch += 32

        self.blk_bna = nn.Sequential(
            nn.BatchNorm2d(unit_in_ch, eps=1e-5),
            nn.ReLU(inplace=True)
        )

    def forward(self, prev_feat):
        for idx in range(self.nr_unit):
            new_feat = self.units[idx](prev_feat)
            prev_feat = torch.cat([prev_feat, new_feat], dim=1)
        prev_feat = self.blk_bna(prev_feat)

        return prev_feat
