import logging
import os
from urllib.request import urlretrieve

import keras
import tensorflow as tf
from kafka import KafkaConsumer

from core.model import load_model, process_document
from database import db_session
from database.models import Picture, Status
from settings import KAFKA_CONSUMER_GROUP, KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, DATA_DIR, MODEL_JSON_PATH, \
    MODEL_WEIGHTS_PATH, MODEL_JSON_URL, MODEL_WEIGHTS_URL

logger = logging.getLogger(__name__)

def process_msg(id, model):
    p = Picture.query.filter(Picture.id == id).one()
    result_path = '{}/{}_result.png'.format(DATA_DIR, id)
    result_mask_path = '{}/{}_mask.png'.format(DATA_DIR, id)
    process_document(model, p.input_path, result_path, result_mask_path)
    p.mask_path = result_mask_path
    p.result_path = result_path
    p.status = Status.DONE
    db_session.commit()


def download_model(path, url):
    if not os.path.exists(path):
        logger.info("Downloading model")
        logger.info("Downloading {}".format(url))
        urlretrieve(url, path)


def check_model_files():
    download_model(MODEL_JSON_PATH, MODEL_JSON_URL)
    download_model(MODEL_WEIGHTS_PATH, MODEL_WEIGHTS_URL)


def main():
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id=KAFKA_CONSUMER_GROUP
        )
        session = tf.Session(graph=tf.Graph())
        with session.graph.as_default():
            keras.backend.set_session(session)

            check_model_files()
            model = load_model(MODEL_JSON_PATH, MODEL_WEIGHTS_PATH)

            logger.info("Start listing")

            for msg in consumer:
                logger.info(msg)
                id = msg.value.decode()
                logger.info("Start processing id : {}".format(id))
                process_msg(id, model)
                consumer.commit()
                logger.info("Finish processing id : {}".format(id))

    finally:
        logger.info("closing db")
        db_session.remove()


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    main()
