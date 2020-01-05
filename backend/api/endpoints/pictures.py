import io
import logging
import uuid

import cv2
from flask import send_file
from flask_restplus import Resource
from werkzeug.utils import secure_filename

import settings
from api.api import api
from api.serializers import picture, upload_parser
from database import db_session
from database.models import Picture
from kafka import KafkaProducer

log = logging.getLogger(__name__)

ns = api.namespace('pictures', description='Operations related to pictures')

DATA_DIR = './data'


@ns.route('/')
class PictureCollection(Resource):

    @api.marshal_list_with(picture)
    def get(self):
        """
        Returns list of pictures.
        """
        pictures = Picture.query.all()
        return pictures

    @api.response(201, 'Picture successfully created.')
    @api.expect(upload_parser)
    @api.marshal_with(picture)
    def post(self):
        """
        Upload a new picture.
        """
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        filename = secure_filename(uploaded_file.filename)
        content_type = uploaded_file.content_type
        id = str(uuid.uuid4())
        file_path = "{}/{}.png".format(DATA_DIR, id)
        logging.info("Recevied file: {} with content type: {}, id: {}".format(filename, content_type, id))
        uploaded_file.save(file_path)
        picture = Picture(id, file_path)
        db_session.add(picture)
        db_session.commit()

        producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        data = str.encode(picture.id)
        producer.send(settings.KAFKA_TOPIC, data)
        producer.flush()

        return picture, 201


@ns.route('/<id>')
@api.doc(params={'id': 'An ID'})
@api.response(404, 'Picture not found.')
class PictureItem(Resource):
    @api.marshal_with(picture)
    def get(self, id):
        """
        Returns picture status.
        """
        return Picture.query.filter(Picture.id == id).one()


@ns.route('/<id>/input')
@api.doc(params={'id': 'An ID'})
@api.response(404, 'Picture not found.')
class PictureInput(Resource):
    def get(self, id):
        """
        Returns a input picture.
        """
        picture = Picture.query.filter(Picture.id == id).one()
        file_path = picture.input_path
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            api.abort(404)
        output = cv2.imencode('.png', img)[1].tobytes()
        return send_file(
            io.BytesIO(output),
            mimetype='image/png'
        )


@ns.route('/<id>/mask')
@api.doc(params={'id': 'An ID'})
@api.response(404, 'Picture not found.')
class PictureMask(Resource):
    def get(self, id):
        """
        Returns a mask picture.
        """
        picture = Picture.query.filter(Picture.id == id).one()
        file_path = picture.mask_path
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            api.abort(404)
        output = cv2.imencode('.png', img)[1].tobytes()
        return send_file(
            io.BytesIO(output),
            mimetype='image/png'
        )

@ns.route('/<id>/result')
@api.doc(params={'id': 'An ID'})
@api.response(404, 'Picture not found.')
class PictureResult(Resource):
    def get(self, id):
        """
        Returns a result picture.
        """
        picture = Picture.query.filter(Picture.id == id).one()
        file_path = picture.result_path
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            api.abort(404)
        output = cv2.imencode('.png', img)[1].tobytes()
        return send_file(
            io.BytesIO(output),
            mimetype='image/png'
        )
