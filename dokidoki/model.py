import timm
import torch
import torch.nn as nn
from fastapi import HTTPException

model = None

class TimmModel(nn.Module):
    """
    Timm 라이브러리를 사용하여 다양한 사전 훈련된 모델을 제공하는 클래스.
    """
    def __init__(
        self,
        model_name: str,
        num_classes: int,
        pretrained: bool
    ):
        super(TimmModel, self).__init__()
        self.model = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=num_classes
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:

        return self.model(x)
    

def load_model(path):
    global model
    
    model = TimmModel(
        pretrained = False,
        num_classes=345,
        model_name='eva02_large_patch14_224.mim_m38m',
    )
    
    model.load_state_dict(
        torch.load(
            path,
            map_location=torch.device('cuda')
        )
    )
    model.eval()


def get_model():
    if model is None:
        raise Exception("Model not found in app state")
    
    return model