import logging
import uuid

from kafka import KafkaProducer
from werkzeug.utils import secure_filename

import settings
from database import db_session
from database.models import Picture

log = logging.getLogger(__name__)

DATA_DIR = './data'


def create_picture(img):
    filename = secure_filename(img.filename)
    content_type = img.content_type
    id = str(uuid.uuid4())
    file_path = "{}/{}.png".format(DATA_DIR, id)
    img.save(file_path)
    picture = Picture(id, file_path)
    db_session.add(picture)
    db_session.commit()

    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    data = str.encode(picture.id)
    producer.send(settings.KAFKA_TOPIC, data)
    producer.flush()

    return picture
