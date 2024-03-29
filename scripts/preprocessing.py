"""preprocessing.py: helper functions and Class for preprocessing."""
import copy
import os
from typing import Callable

import numpy as np

import albumentations as albu

from matplotlib import image as mpimg
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
from scripts.array_manipulations import simplify_array

IMG_PATCH_SIZE = 16


class RoadDataset(Dataset):
    """
    Dataset class for preprocessing and delivering satellite images.

    :param image_paths: local absolute path of images
    :param mask_paths: local absolute path of ground truths
    :param transform: Albumentations obj for transforms
    :param preprocess: to adjust the transforms to encoder
    """

    def __init__(self, image_paths, mask_paths=None, transform=None, preprocess=None):
        # read images in
        self.images = [mpimg.imread(path) for path in image_paths]
        self.masks = [mpimg.imread(path) for path in mask_paths] if mask_paths else None

        self.transform = transform
        self.preprocess = preprocess

    def __getitem__(self, i):
        """Getter for providing images to DataLoader."""
        image = self.images[i]
        # if no mask use dummy mask
        mask = (
            np.where(self.masks[i] >= 0.5, 1, 0).astype(np.uint8)
            if self.masks
            else np.zeros(image.shape)
        )

        if self.transform:
            # apply same transformation to image and mask
            # NB! This must be done before converting to Pytorch format
            transformed = self.transform(image=image, mask=mask)
            image, mask = transformed["image"], transformed["mask"]

        # apply preprocessing to adjust to encoder
        if self.preprocess:
            sample = self.preprocess(image=image, mask=mask)
            image, mask = sample["image"], sample["mask"]

        # convert to Pytorch format HWC -> CHW
        image = np.moveaxis(image, -1, 0)
        mask = np.expand_dims(mask, 0)

        return image, mask

    def set_tf(self, transform):
        """Used for transformations.ipynb, where we want to set the transforms
        dynamically for train and validation. This way we can keep the original
        object and return a deepcopy with new transform."""
        copy_instance = copy.deepcopy(self)
        copy_instance.transform = transform
        return copy_instance

    def __len__(self):
        return len(self.images)


def split_data(images_path: str, test_size: float):
    """
    Split list of absolute paths to train and test data by using sklearn.

    :param images_path: absolute path of the parent directory of images
    :param test_size: value [0, 1]
    :return: image_path_train, image_path_test, mask_path_train, mask_path_test
    """
    # specify image and ground truth full path
    image_directory = os.path.join(images_path, "images")
    labels_directory = os.path.join(images_path, "masks")

    # specify absolute paths for all files
    image_paths = [
        os.path.join(image_directory, image)
        for image in sorted(os.listdir(image_directory))
    ]
    mask_paths = [
        os.path.join(labels_directory, image)
        for image in sorted(os.listdir(labels_directory))
    ]

    # All images in train set, none in test
    if test_size == 0:
        return image_paths, [], mask_paths, []
    else:
        return train_test_split(image_paths, mask_paths, test_size=test_size)


def get_class(array: np.ndarray, foreground_threshold: int = 0.25) -> int:
    """
    Based on the specified threshold (by professors) assign the array to
        either foreground/road (1) or background (0).

    :param array: usually a block with shape (16, 16)
    :param foreground_threshold: value over which we consider it to be road
    :return: {0, 1}
    """
    # percentage of pixels > 1 required to assign a foreground label to a patch
    return int(np.mean(array) > foreground_threshold)


def get_patched_classification(array: np.ndarray) -> np.ndarray:
    """
    As the goal is to return label for 16x16 pixel patches, this function helps to
        patch the ground truth or prediction using this logic

    :param array: of shape (1, x, x) or (x, x)
    :return: same size array with same classification value for the patch
    """
    # function name is misleading, but (1, x, x) -> (x, x)
    array = simplify_array(array)
    patched_img = np.zeros(array.shape)

    for x in range(0, array.shape[0], IMG_PATCH_SIZE):
        for y in range(0, array.shape[1], IMG_PATCH_SIZE):
            patched_img[y : y + IMG_PATCH_SIZE, x : x + IMG_PATCH_SIZE] = get_class(
                array[y : y + IMG_PATCH_SIZE, x : x + IMG_PATCH_SIZE]
            )

    return patched_img


def get_preprocessing(preprocessing_fn: Callable):
    """
    Construct preprocessing transform.
            Taken from: https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb

    :param preprocessing_fn: data normalization function
    :return: albumentations.Compose
    """
    _transform = [albu.Lambda(image=preprocessing_fn)]
    return albu.Compose(_transform)
