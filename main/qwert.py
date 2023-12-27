url = 'https://figshare.com/ndownloader/files/34488599'
import numpy as np
import os
import math
# Importing the required packages
import os
import time
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from functools import partial

import albumentations as A
import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision
import torchvision.transforms as T
from albumentations.pytorch import ToTensorV2
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision.models.detection import _utils as det_utils
from torchvision.models.detection.ssdlite import SSDLiteClassificationHead

import deepchecks
# from deepchecks.vision.detection_data import DetectionData
urllib.request.urlretrieve(url, 'tomato-detection.zip')

with zipfile.ZipFile('tomato-detection.zip', 'r') as zip_ref:
    zip_ref.extractall('.')

class TomatoDataset(Dataset):
    def __init__(self, root, transforms):
        self.root = root
        self.transforms = transforms

        self.images = list(sorted(os.listdir(os.path.join(root, 'images'))))
        self.annotations = list(sorted(os.listdir(os.path.join(root, 'annotations'))))

    def __getitem__(self, idx):
        img_path = os.path.join(self.root, "images", self.images[idx])
        ann_path = os.path.join(self.root, "annotations", self.annotations[idx])
        img = Image.open(img_path).convert("RGB")
        bboxes = []
        labels = []
        with open(ann_path, 'r') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)

            for obj in root.iter('object'):
                difficult = obj.find('difficult').text
                if int(difficult) == 1:
                    continue
                cls_id = 1
                xmlbox = obj.find('bndbox')
                b = [float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text),
                        float(xmlbox.find('ymax').text)]
                bboxes.append(b)
                labels.append(cls_id)

        bboxes = torch.as_tensor(np.array(bboxes), dtype=torch.float32)
        labels = torch.as_tensor(np.array(labels), dtype=torch.int64)

        if self.transforms is not None:
            res = self.transforms(image=np.array(img), bboxes=bboxes, class_labels=labels)

        target = {
            'boxes': [torch.Tensor(x) for x in res['bboxes']],
            'labels': res['class_labels']
        }

        img = res['image']

        return img, target

    def __len__(self):
        return len(self.images)

data_transforms = A.Compose([
    A.Resize(height=256, width=256),
    A.CenterCrop(height=224, width=224),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['class_labels']))

dataset = TomatoDataset(root=os.path.join(os.path.curdir, 'tomato-detection/data'),
                        transforms=data_transforms)
train_set, val_set = torch.utils.data.random_split(dataset,
                                                    [int(len(dataset)*0.9), len(dataset)-int(len(dataset)*0.9)],
                                                    generator=torch.Generator().manual_seed(42))
val_set.transforms = A.Compose([ToTensorV2()])
train_loader = DataLoader(train_set, batch_size=64, collate_fn=(lambda batch: tuple(zip(*batch))))
val_loader = DataLoader(val_set, batch_size=64, collate_fn=(lambda batch: tuple(zip(*batch))))