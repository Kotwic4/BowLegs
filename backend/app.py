import io
import logging
import uuid

import cv2
import werkzeug
from flask import Flask, send_file
from flask_restplus import Api, Resource
from werkzeug.datastructures import FileStorage

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='BowLegs',
          description='API for detection bows in legs pictures',
          )

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

DATA_DIR = './data'


@api.route('/upload')
@api.expect(upload_parser)
class Upload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        filename = werkzeug.secure_filename(uploaded_file.filename)
        content_type = uploaded_file.content_type

        ext = filename.split('.')[-1]
        id = str(uuid.uuid4())
        file_path = "{}/{}.png".format(DATA_DIR, id)

        logging.info("Recevied file: {} with content type: {}, id: {}".format(filename, content_type, id))

        uploaded_file.save(file_path)
        return {'id': id}, 201

@api.route('/input')
class Input(Resource):
    def get(self):
        return []

@api.route('/input/<id>')
@api.doc(params={'id': 'An ID'})
class SingleInput(Resource):
    @api.response(404, 'Not Found')
    def get(self, id):
        logging.info(id)
        file_path = "{}/{}.png".format(DATA_DIR, id)
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            api.abort(404)
        output = cv2.imencode('.png', img)[1].tobytes()
        return send_file(
            io.BytesIO(output),
            mimetype='image/png'
        )


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    app.run(debug=True)
