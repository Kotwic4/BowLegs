# Flask settings
import os

FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'FALSE') != 'FALSE'  # Do not use debug mode in production
PORT = int(os.getenv('PORT', '8888'))

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///data/db.sqlite')

# KAFKA
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'bow_legs')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP', 'bow_legs_worker')

# Data
DATA_DIR = os.getenv('DATA_DIR', './data')

# Models
MODEL_JSON_URL = os.getenv('MODEL_JSON_URL', 'https://github.com/Kotwic4/BowLegs/releases/download/1.1/model_bk.json')
MODEL_WEIGHTS_URL = os.getenv('MODEL_WEIGHTS_URL',
                              'https://github.com/Kotwic4/BowLegs/releases/download/1.1/trained_model.hdf5')
MODEL_JSON_PATH = os.getenv('MODEL_JSON_PATH', './model/model.json')
MODEL_WEIGHTS_PATH = os.getenv('MODEL_WEIGHTS_PATH', './model/model.hdf5')
