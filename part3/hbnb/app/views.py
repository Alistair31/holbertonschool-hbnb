import os
from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__), 'static', 'images', 'places'
)
AMENITY_UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__), 'static', 'images', 'amenities'
)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


views = Blueprint('views', __name__)


@views.route('/')
@views.route('/index')
def index():
    return render_template('index.html')


@views.route('/login')
def login():
    return render_template('login.html')


@views.route('/place')
def place():
    return render_template('place.html')


@views.route('/register')
def register():
    return render_template('register.html')


@views.route('/add_review')
def add_review():
    return render_template('add_review.html')


@views.route('/create_place')
def create_place():
    return render_template('create_place.html')


@views.route('/upload_images/<place_id>', methods=['POST'])
@jwt_required()
def upload_images(place_id):
    from app.services import facade
    from app import db
    from app.models.place_image import PlaceImage

    place = facade.get_place(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    files = request.files.getlist('images')
    if not files:
        return jsonify({'error': 'No files provided'}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    uploaded = []
    is_first = not place.images

    for file in files:
        if file.filename == '' or not allowed_file(file.filename):
            continue
        filename = secure_filename(f"{place_id}_{file.filename}")
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        image_url = f"/static/images/places/{filename}"
        img = PlaceImage(
            place_id=place_id,
            image_url=image_url,
            is_primary=is_first
        )
        db.session.add(img)
        uploaded.append(image_url)
        is_first = False

    db.session.commit()
    return jsonify({'images': uploaded}), 200


@views.route('/upload_amenity_icon/<amenity_id>', methods=['POST'])
@jwt_required()
def upload_amenity_icon(amenity_id):
    from app.services import facade
    from app import db

    claims = get_jwt_identity()
    from flask_jwt_extended import get_jwt
    if not get_jwt().get('is_admin'):
        return jsonify({'error': 'Admin privileges required'}), 403

    amenity = facade.get_amenity(amenity_id)
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404

    file = request.files.get('icon')
    if not file or file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400

    os.makedirs(AMENITY_UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(f"amenity_{amenity_id}.{file.filename.rsplit('.', 1)[1].lower()}")
    file.save(os.path.join(AMENITY_UPLOAD_FOLDER, filename))
    icon_url = f"/static/images/amenities/{filename}"
    amenity.icon_url = icon_url
    db.session.commit()
    return jsonify({'icon_url': icon_url}), 200


@views.route('/place_images/<place_id>', methods=['GET'])
def get_place_images(place_id):
    from app.services import facade
    place = facade.get_place(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify([{
        'id': img.id,
        'image_url': img.image_url,
        'is_primary': img.is_primary
    } for img in place.images]), 200
