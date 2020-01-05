import logging
import os
import os.path

import cv2
import keras
import numpy as np
import tensorflow as tf
from keras.models import model_from_json
from skimage import img_as_ubyte
from skimage import morphology, color
from skimage import transform

INPUT_SHAPE = (512, 256)


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


def load_model(model_json_path, model_weights_path):
    logging.info("Loading model json from: {}".format(model_json_path))
    with open(model_json_path, 'r') as json_file:
        loaded_model_json = json_file.read()
    model = model_from_json(loaded_model_json)

    logging.info("Loading model weight from: {}".format(model_weights_path))
    model.load_weights(model_weights_path)

    logging.info("Loaded model from disk")
    return model


def grey_scale_image(image):
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        return image


def process_mask(mask):
    pr = mask > 0.5
    pr = remove_small_regions(pr, 0.005 * np.prod(mask.shape))
    return pr


def predict(input, model):
    height, width = input.shape[:2]
    grey_scale = grey_scale_image(input)
    img = transform.resize(grey_scale[:, :], INPUT_SHAPE, mode='constant')
    img = np.expand_dims(img, -1)
    img -= img.mean()
    img /= img.std()

    xx = img[:, :, :][None, ...]

    pred = model.predict(xx)[..., 0].reshape(img.shape[:2])
    pr = process_mask(pred)

    pr_bin = img_as_ubyte(pr)
    pr_openned = morphology.opening(pr_bin)

    resized_mask = cv2.resize(pr_openned, (width, height))
    masked_image = masked(grey_scale, resized_mask > 0.5, alpha=0.5)
    rgb_image = cv2.cvtColor(img_as_ubyte(masked_image), cv2.COLOR_BGR2RGB)

    return rgb_image, resized_mask


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


def process_document(model, img_path, result_path, result_mask_path=None):
    img = load_img(img_path)
    result, result_mask = predict(img, model)
    save_img(result, result_path)
    if result_mask_path is not None:
        save_img(result_mask, result_mask_path)


def compare_mask(pr_mask_path, gt_mask_path):
    pr = load_img(pr_mask_path)
    gt = load_img(gt_mask_path)

    pr = process_mask(pr)
    gt = process_mask(gt)

    return iou(gt, pr), dice(gt, pr)


def mask_gt_and_pr(img_path, pr_mask_path, gt_mask_path):
    img = load_img(img_path)
    pr = load_img(pr_mask_path)
    gt = load_img(gt_mask_path)

    pr = process_mask(pr)
    gt = process_mask(gt)

    grey_scale = grey_scale_image(img)

    masked_image = masked(grey_scale, pr, gt=gt, alpha=0.5)
    rgb_image = cv2.cvtColor(img_as_ubyte(masked_image), cv2.COLOR_BGR2RGB)

    return rgb_image


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    input_dir = './data'
    result_dir = './result'
    model_dir = './model'

    inputs = [
        ("test1.png", "test1_mask.png"),
        ("test2.png", "test2_mask.png"),
        ("test5.jpg", None),
    ]

    session = tf.Session(graph=tf.Graph())
    with session.graph.as_default():
        keras.backend.set_session(session)
        model_json_path = '{}/model_bk.json'.format(model_dir)
        model_weights_path = '{}/trained_model.hdf5'.format(model_dir)
        model = load_model(model_json_path, model_weights_path)

        for img_name, mask_name in inputs:
            img_path = '{}/{}'.format(input_dir, img_name)
            img_name = '.'.join(img_name.split('.')[:-1])
            result_path = '{}/{}.png'.format(result_dir, img_name)
            result_mask_path = '{}/{}_mask.png'.format(result_dir, img_name)
            process_document(model, img_path, result_path, result_mask_path)

            if mask_name is not None:
                gt_mask_path = '{}/{}'.format(input_dir, mask_name)
                result_gt_mask_path = '{}/{}_gt_mask.png'.format(result_dir, img_name)
                print(compare_mask(result_mask_path, gt_mask_path))
                img = mask_gt_and_pr(img_path, result_mask_path, gt_mask_path)
                save_img(img, result_gt_mask_path)


if __name__ == '__main__':
    main()
