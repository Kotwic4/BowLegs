# Flask settings
FLASK_DEBUG = False  # Do not use debug mode in production
PORT = 8888

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/db.sqlite'

# KAFKA
KAFKA_TOPIC = 'bow_legs'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
