import logging
import os
import os.path

import cv2
import numpy as np
from skimage import img_as_ubyte
from skimage import morphology, color

def load_img(im_path: str):
    logging.info("Loading image from: {}".format(im_path))
    if not os.path.exists(im_path):
        raise ValueError("File not found: {}".format(im_path))
    img = cv2.imread(im_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError("Could not process image from: {}".format(im_path))
    return img


def masked(img, mask, gt=None, alpha=1.):
    """Returns image with GT lung field outlined with red, predicted lung field filled with blue."""
    rows, cols = img.shape[:2]
    color_mask = np.zeros((rows, cols, 3))

    if gt is not None:
        boundary = morphology.dilation(gt, morphology.disk(3)) ^ gt
        color_mask[boundary == 1] = [1, 0, 0]

    color_mask[mask == 1] = [0, 0, 1]
    img_color = np.dstack((img, img, img))

    img_hsv = color.rgb2hsv(img_color)
    color_mask_hsv = color.rgb2hsv(color_mask)

    img_hsv[..., 0] = color_mask_hsv[..., 0]
    img_hsv[..., 1] = color_mask_hsv[..., 1] * alpha

    img_masked = color.hsv2rgb(img_hsv)
    return img_masked


def remove_small_regions(img, size):
    """Morphologically removes small (less than size) connected regions of 0s or 1s."""
    img = morphology.remove_small_objects(img, size)
    img = morphology.remove_small_holes(img, size)
    return img


def grey_scale_image(image):
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        return image


def process_mask(mask):
    pr = mask > 0.5
    pr = remove_small_regions(pr, 0.005 * np.prod(mask.shape))
    return pr


def save_img(result, result_path):
    logging.info("Saving image from: {}".format(result_path))
    result_dir = os.path.dirname(result_path)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    cv2.imwrite(result_path, result)


def iou(y_true, y_pred):
    """Returns Intersection over Union score for ground truth and predicted masks."""
    assert y_true.dtype == bool and y_pred.dtype == bool
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.logical_and(y_true_f, y_pred_f).sum()
    union = np.logical_or(y_true_f, y_pred_f).sum()
    return (intersection + 1) * 1. / (union + 1)


def dice(y_true, y_pred):
    """Returns Dice Similarity Coefficient for ground truth and predicted masks."""
    assert y_true.dtype == bool and y_pred.dtype == bool
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.logical_and(y_true_f, y_pred_f).sum()
    return (2. * intersection + 1.) / (y_true.sum() + y_pred.sum() + 1.)


def compare_mask(pr, gt):
    pr = process_mask(pr)
    gt = process_mask(gt)

    return iou(gt, pr), dice(gt, pr)


def mask_gt_and_pr(img, pr, gt):
    pr = process_mask(pr)
    gt = process_mask(gt)

    grey_scale = grey_scale_image(img)

    masked_image = masked(grey_scale, pr, gt=gt, alpha=0.5)
    rgb_image = cv2.cvtColor(img_as_ubyte(masked_image), cv2.COLOR_BGR2RGB)

    return rgb_image
