import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Hyperparameters etc.
LEARNING_RATE = 1e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 4
NUM_EPOCHS = 30
NUM_WORKERS = 0
IMAGE_HEIGHT = 256
IMAGE_WIDTH = 256
PIN_MEMORY = True
LOAD_MODEL = False
TRAIN_IMG_DIR = "Dataset_Unet/train_images/"
TRAIN_MASK_DIR = "Dataset_Unet/train_masks/"
VAL_IMG_DIR = "Dataset_Unet/val_images/"
VAL_MASK_DIR = "Dataset_Unet/val_masks/"

CHECKPOINT_FILE_NAME = "my_checkpoint.pth.tar"
FOLDER_NAME_TO_SAVE_IMAGES = 'saved_images/'

# Transforms

train_transform = A.Compose(
        [
            A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
            A.Rotate(limit=35, p=1.0),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.1),
            A.Normalize(
                mean=[0.0, 0.0, 0.0],
                std=[1.0, 1.0, 1.0],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )


val_transforms = A.Compose(
        [
            A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
            A.Normalize(
                mean=[0.0, 0.0, 0.0],
                std=[1.0, 1.0, 1.0],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )