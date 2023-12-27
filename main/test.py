import numpy as np
import pandas as pd

from torch import nn

from PIL import Image

from torchvision import models
from torchvision import transforms

class Dataset:
    def __init__(self, path, domain):
        self.dataset = pd.read_excel(path, sheet_name='main').to_numpy()

        transform_dict = {
            'train': transforms.Compose(
                [
                    transforms.Resize(224),
                    transforms.RandomCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ]
            ),
            'test': transforms.Compose(
                [
                    transforms.Resize(224),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ]
            )
        }

        self.domain = domain
        self.transform = transform_dict[domain]

    def __getitem__(self, i):
        path, flame, smoke = self.dataset[i]

        image = Image.open(path).convert('RGB')
        image = self.transform(image)

        label = np.asarray([flame, smoke], dtype=np.float32)

        if self.domain == 'train':
            return image, label
        else:
            return path, image
    
    def __len__(self):
        return len(self.dataset)

class Network(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        self.backbone = models.detection.ssdlite320_mobilenet_v3_large(num_classes=1,
        weights=None,
        weights_backbone=None)
        self.backbone.classifier = nn.Linear(in_features=1280, out_features=num_classes)

    def forward(self, images):
        return self.backbone(images)
    