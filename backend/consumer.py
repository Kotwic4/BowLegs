import logging

import keras
import tensorflow as tf
from kafka import KafkaConsumer

from database import db_session
from database.models import Picture, Status
from model import load_model, process_document

KAFKA_TOPIC_NAME = 'bow_legs'
KAFKA_CONSUMER_GROUP = 'bow_legs_worker'
MODEL_DIR = './model'
DATA_DIR = './data'

if __name__ == '__main__':
    try:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        consumer = KafkaConsumer(
            KAFKA_TOPIC_NAME,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id=KAFKA_CONSUMER_GROUP
        )
        session = tf.Session(graph=tf.Graph())
        with session.graph.as_default():
            keras.backend.set_session(session)
            model_json_path = '{}/model_bk.json'.format(MODEL_DIR)
            model_weights_path = '{}/trained_model.hdf5'.format(MODEL_DIR)

            model = load_model(model_json_path, model_weights_path)

            for msg in consumer:
                logger.info(msg)
                id = msg.value.decode()
                logger.info("Start processing id : {}".format(id))

                p = Picture.query.filter(Picture.id == id).one()
                result_path = '{}/{}_result.png'.format(DATA_DIR, id)
                result_mask_path = '{}/{}_mask.png'.format(DATA_DIR, id)
                process_document(model, p.input_path, result_path, result_mask_path)
                p.mask_path = result_mask_path
                p.result_path = result_path
                p.status = Status.DONE
                db_session.commit()
                consumer.commit()

                logger.info("Finish processing id : {}".format(id))
    finally:
        print("closing db")
        db_session.remove()
