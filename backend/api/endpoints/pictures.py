import io
import logging

import cv2
from flask import send_file
from flask_restplus import Resource

from api.api import api
from api.controlers.pictures import create_picture
from api.serializers import picture, upload_parser
from database.models import Picture

import numpy as np

from core.image_processing import compare_mask, mask_gt_and_pr

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
        picture = create_picture(uploaded_file)
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


def load_picture(id, key):
    picture = Picture.query.filter(Picture.id == id).one()
    file_path = getattr(picture, key)
    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        api.abort(404)
    return img


def return_img(img):
    output = cv2.imencode('.png', img)[1].tobytes()
    return send_file(
        io.BytesIO(output),
        mimetype='image/png'
    )


def get_picture_img(id, key):
    img = load_picture(id, key)
    return return_img(img)


@ns.route('/<id>/input')
@api.doc(params={'id': 'An ID'})
@api.response(404, 'Picture not found.')
class PictureInput(Resource):
    def get(self, id):
        """
        Returns a input picture.
        """
        return get_picture_img(id, 'input_path')

def process_gt_input(uploaded_file):
    in_memory_file = io.BytesIO()
    uploaded_file.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_UNCHANGED)

@ns.route('/<id>/mask')
@api.doc(params={'id': 'An ID'})
@api.response(404, 'Picture not found.')
class PictureMask(Resource):
    def get(self, id):
        """
        Returns a mask picture.
        """
        return get_picture_img(id, 'mask_path')

    @api.expect(upload_parser)
    def post(self, id):
        """
        Compare picture mask.
        """
        args = upload_parser.parse_args()
        uploaded_file = args['file']

        gt = process_gt_input(uploaded_file)
        pr = load_picture(id, 'mask_path')

        iou, dice = compare_mask(pr, gt)

        return {'iou': iou, 'dice': dice}


@ns.route('/<id>/result')
@api.doc(params={'id': 'An ID'})
@api.response(404, 'Picture not found.')
class PictureResult(Resource):
    def get(self, id):
        """
        Returns a mask picture.
        """
        return get_picture_img(id, 'result_path')

    @api.expect(upload_parser)
    def post(self, id):
        """
        Mark prediction and golden source.
        """
        args = upload_parser.parse_args()
        uploaded_file = args['file']

        gt = process_gt_input(uploaded_file)
        pr = load_picture(id, 'mask_path')
        img = load_picture(id, 'input_path')

        result = mask_gt_and_pr(img, pr, gt)

        return return_img(result)
