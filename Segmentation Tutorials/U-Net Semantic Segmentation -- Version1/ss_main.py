from ss_model import UNet
import torch
import torch.nn as nn
import torch.optim as optim
from ss_utils import load_checkpoint, save_checkpoint, get_loaders, check_accuracy, save_predictions_as_imgs
import ss_config
from ss_train import train_fn


def main():
    net = UNet(n_channels=3, n_classes=1).to(ss_config.DEVICE)

    # loss_fn = nn.CrossEntropyLoss()
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(net.parameters(), lr=ss_config.LEARNING_RATE)

    train_loader, val_loader = get_loaders(
        ss_config.TRAIN_IMG_DIR,
        ss_config.TRAIN_MASK_DIR,
        ss_config.VAL_IMG_DIR,
        ss_config.VAL_MASK_DIR,
        ss_config.BATCH_SIZE,
        ss_config.train_transform,
        ss_config.val_transforms,
        ss_config.NUM_WORKERS,
        ss_config.PIN_MEMORY,
    )

    if ss_config.LOAD_MODEL:
        load_checkpoint(torch.load(ss_config.CHECKPOINT_FILE_NAME), net)

    check_accuracy(val_loader, net, device=ss_config.DEVICE)
    scaler = torch.cuda.amp.GradScaler()

    for epoch in range(ss_config.NUM_EPOCHS):
        train_fn(train_loader, net, optimizer, loss_fn, scaler)

        # save model
        checkpoint = {
            "state_dict": net.state_dict(),
            "optimizer": optimizer.state_dict(),
        }
        save_checkpoint(checkpoint)

        # check accuracy
        check_accuracy(val_loader, net, device=ss_config.DEVICE)

        # print some examples to a folder
        save_predictions_as_imgs(
            val_loader, net, folder=ss_config.FOLDER_NAME_TO_SAVE_IMAGES, device=ss_config.DEVICE
        )


if __name__ == '__main__':
    main()