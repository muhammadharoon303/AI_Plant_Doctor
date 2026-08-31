import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models

class PlantDiseaseClassifier(nn.Module):
    """
    PyTorch Convolutional Neural Network backbone for plant disease classification.
    Supports transfer learning (ResNet18, MobileNetV3) or custom lightweight CNN.
    """
    def __init__(self, num_classes: int = 10, use_transfer_learning: bool = True, backbone: str = "resnet18"):
        super(PlantDiseaseClassifier, self).__init__()
        self.num_classes = num_classes
        self.use_transfer_learning = use_transfer_learning
        self.backbone = backbone

        if use_transfer_learning:
            if backbone == "resnet18":
                self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
                in_features = self.model.fc.in_features
                self.model.fc = nn.Linear(in_features, num_classes)
            elif backbone == "mobilenet_v3":
                self.model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
                in_features = self.model.classifier[3].in_features
                self.model.classifier[3] = nn.Linear(in_features, num_classes)
            else:
                self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
                in_features = self.model.fc.in_features
                self.model.fc = nn.Linear(in_features, num_classes)
        else:
            # Custom Lightweight CNN Architecture
            self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
            self.bn1 = nn.BatchNorm2d(32)
            self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
            self.bn2 = nn.BatchNorm2d(64)
            self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
            self.bn3 = nn.BatchNorm2d(128)
            self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
            self.bn4 = nn.BatchNorm2d(256)
            
            self.pool = nn.MaxPool2d(2, 2)
            self.dropout = nn.Dropout(0.4)
            self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
            
            self.fc1 = nn.Linear(256 * 7 * 7, 512)
            self.fc2 = nn.Linear(512, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.use_transfer_learning:
            return self.model(x)

        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = self.pool(F.relu(self.bn4(self.conv4(x))))
        
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.dropout(F.relu(self.fc1(x)))
        logits = self.fc2(x)
        return logits
