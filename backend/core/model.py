import logging

import cv2
import numpy as np
from keras.models import model_from_json
from skimage import img_as_ubyte
from skimage import morphology
from skimage import transform

from core.image_processing import grey_scale_image, process_mask, masked, load_img, save_img

INPUT_SHAPE = (512, 256)


def load_model(model_json_path, model_weights_path):
    logging.info("Loading model json from: {}".format(model_json_path))
    with open(model_json_path, 'r') as json_file:
        loaded_model_json = json_file.read()
    model = model_from_json(loaded_model_json)

    logging.info("Loading model weight from: {}".format(model_weights_path))
    model.load_weights(model_weights_path)

    logging.info("Loaded model from disk")
    return model


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


def process_document(model, img_path, result_path, result_mask_path=None):
    img = load_img(img_path)
    result, result_mask = predict(img, model)
    save_img(result, result_path)
    if result_mask_path is not None:
        save_img(result_mask, result_mask_path)
