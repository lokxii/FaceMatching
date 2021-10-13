import torch
import torch.nn as nn
import torch.nn.functional as F
# 2021-07-31-10_22_13
# Accuracy 82

activ = F.relu

class ConvNet(nn.Module):

    def __init__(self):
        super(ConvNet, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.norm1 = nn.BatchNorm2d(32)
        
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1)
        self.norm2 = nn.BatchNorm2d(32)

        self.max_pool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.norm3 = nn.BatchNorm2d(64)

        self.conv4 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.norm4 = nn.BatchNorm2d(128)

        self.max_pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv5 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1)
        self.norm5 = nn.BatchNorm2d(256)

        self.conv6 = nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, padding=1)
        self.norm6 = nn.BatchNorm2d(512)

        self.oc = 512

        self.avg_pool = nn.AvgPool2d(kernel_size=8)

    def forward(self, x):
        x = activ( self.norm1( self.conv1(x) ) )
        x = activ( self.norm2( self.conv2(x) ) )
        x = self.max_pool(x)
        x = activ( self.norm3( self.conv3(x) ) )
        x = activ( self.norm4( self.conv4(x) ) )
        x = self.max_pool1(x)
        x = activ( self.norm5( self.conv5(x) ) )
        x = activ( self.norm6( self.conv6(x) ) )
        x = self.avg_pool(x)
        x = x.view(-1, self.oc)
        return x

class FCNet(nn.Module):
    def __init__(self, inSize):
        super(FCNet, self).__init__()
        self.fc1 = nn.Linear(inSize, inSize)
        self.drop = nn.Dropout(0.6)

        self.fc2 = nn.Linear(inSize, 1)

    def forward(self, x):
        x = activ(self.fc1(x))
        x = self.drop(x)
        x = self.fc2(x)
        x = torch.sigmoid(x)
        return x

class SiameseNet(nn.Module):
    def __init__(self):
        super(SiameseNet, self).__init__()
        self.conv = ConvNet()
        self.fc = FCNet(self.conv.oc)

    def aggregate(self, h1, h2):
        return torch.abs(torch.sub(h1, h2))

    def forward(self, x):
        h1 = self.conv(x[0])
        h2 = self.conv(x[1])
        x = self.aggregate(h1, h2)
        x = self.fc(x)
        x = torch.flatten(x)
        return x

def save_checkpoint(path, model, optimizer):
    state_dict = {
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
    }
    torch.save(state_dict, path)
    print(f"Model saved to {path}")

def load_checkpoint(path, model, optimizer=None):
    state_dict = torch.load(path, map_location="cpu")
    model.load_state_dict(state_dict["model_state"])
    if optimizer != None:
        optimizer.load_state_dict(state_dict["optimizer_state"])
    print(f"Model loaded from {path}")
