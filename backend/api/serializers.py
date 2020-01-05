from flask_restplus import fields
from api.api import api
from werkzeug.datastructures import FileStorage

picture = api.model('Picture', {
    'id': fields.String(readOnly=True, description='The unique identifier of a picture'),
    'status': fields.String(readOnly=True, description='Current status of a picture processing')
})

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)