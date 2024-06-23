from flask import request, jsonify, Blueprint
from models import db, User, Kegiatan, PersonalTask, Review, Catatan
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return "hello"

# User Registration
@routes.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(nama=data['nama'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# User Login
@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=user.user_id)
    return jsonify(access_token=access_token), 200

@routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({'user': user.nama}), 200

# User Routes
@routes.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(nama=data['nama'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@routes.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{'user_id': user.user_id, 'nama': user.nama, 'email': user.email} for user in users])

@routes.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'user_id': user.user_id, 'nama': user.nama, 'email': user.email})

@routes.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.nama = data.get('nama', user.nama)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@routes.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# Event Routes
from datetime import datetime

@routes.route('/events', methods=['POST'])
@jwt_required() 
def create_event():
    tanggal = request.json.get('tanggal')
    
    try:
        parsed_date = datetime.strptime(tanggal, '%Y-%m-%dT%H:%M')
    except ValueError as e:
        return jsonify({'error': 'Invalid datetime format', 'details': str(e)}), 400
    
    new_event = Kegiatan(
        user_id=request.json.get('user_id'),
        judul=request.json.get('judul'),
        deskripsi=request.json.get('deskripsi'),
        tanggal=parsed_date,
        tempat=request.json.get('tempat')
    )
    db.session.add(new_event)
    db.session.commit()
    
    return jsonify({'message': 'Event created successfully'}), 201


@routes.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    events = Kegiatan.query.all()
    return jsonify([{
        'kegiatan_id': event.kegiatan_id,
        'user_id': event.user_id,
        'judul': event.judul,
        'deskripsi': event.deskripsi,
        'tanggal': event.tanggal,
        'tempat': event.tempat
    } for event in events])

@routes.route('/events/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    event = Kegiatan.query.get_or_404(event_id)
    return jsonify({
        'kegiatan_id': event.kegiatan_id,
        'user_id': event.user_id,
        'judul': event.judul,
        'deskripsi': event.deskripsi,
        'tanggal': event.tanggal,
        'tempat': event.tempat
    })

@routes.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    event = Kegiatan.query.get_or_404(event_id)
    data = request.json
    event.judul = data.get('judul', event.judul)
    event.deskripsi = data.get('deskripsi', event.deskripsi)
    date_string = request.json.get('tanggal')
    event.tanggal = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    event.tempat = data.get('tempat', event.tempat)
    db.session.commit()
    return jsonify({'message': 'Event updated successfully'})

@routes.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    event = Kegiatan.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'})

# PersonalTask Routes
@routes.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.json
    date_format = "%Y-%m-%d %H:%M:%S"
    new_task = PersonalTask(
        user_id=data['user_id'],
        task_description=data['task_description'],
        due_date=datetime.strptime(data['due_date'], date_format),
        status=data['status']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201

@routes.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = PersonalTask.query.all()
    return jsonify([{
        'task_id': task.task_id,
        'user_id': task.user_id,
        'task_description': task.task_description,
        'due_date': task.due_date,
        'status': task.status
    } for task in tasks])

@routes.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    task = PersonalTask.query.get_or_404(task_id)
    return jsonify({
        'task_id': task.task_id,
        'user_id': task.user_id,
        'task_description': task.task_description,
        'due_date': task.due_date,
        'status': task.status
    })

@routes.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = PersonalTask.query.get_or_404(task_id)
    data = request.json
    task.task_description = data.get('task_description', task.task_description)
    date_string = request.json.get('due_date')
    task.due_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@routes.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = PersonalTask.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

# Review Routes
@routes.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    data = request.json
    date_format = "%Y-%m-%d %H:%M:%S"
    new_review = Review(
        user_id=data['user_id'],
        kegiatan_id=data['kegiatan_id'],
        rating=data['rating'],
        komentar=data.get('komentar'),
        tanggal_review=datetime.strptime(data['tanggal_review'], date_format),
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review created successfully'}), 201

@routes.route('/reviews', methods=['GET'])
@jwt_required()
def get_reviews():
    reviews = Review.query.all()
    return jsonify([{
        'review_id': review.review_id,
        'user_id': review.user_id,
        'kegiatan_id': review.kegiatan_id,
        'rating': review.rating,
        'komentar': review.komentar,
        'tanggal_review': review.tanggal_review
    } for review in reviews])

@routes.route('/reviews/<int:review_id>', methods=['GET'])
@jwt_required()
def get_review(review_id):
    review = Review.query.get_or_404(review_id)
    return jsonify({
        'review_id': review.review_id,
        'user_id': review.user_id,
        'kegiatan_id': review.kegiatan_id,
        'rating': review.rating,
        'komentar': review.komentar,
        'tanggal_review': review.tanggal_review
    })

@routes.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    data = request.json
    review.rating = data.get('rating', review.rating)
    review.komentar = data.get('komentar', review.komentar)
    date_string = request.json.get('tanggal_review')
    review.tanggal_review = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    db.session.commit()
    return jsonify({'message': 'Review updated successfully'})

@routes.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'})

# Catatan Routes
@routes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    data = request.json
    new_note = Catatan(
        user_id=data['user_id'],
        catatan=data['catatan']
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note created successfully'}), 201

@routes.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    notes = Catatan.query.all()
    return jsonify([{
        'catatan_id': note.catatan_id,
        'user_id': note.user_id,
        'catatan': note.catatan
    } for note in notes])

@routes.route('/notes/<int:catatan_id>', methods=['GET'])
@jwt_required()
def get_note(catatan_id):
    note = Catatan.query.get_or_404(catatan_id)
    return jsonify({
        'catatan_id': note.catatan_id,
        'user_id': note.user_id,
        'catatan': note.catatan
    })

@routes.route('/notes/<int:catatan_id>', methods=['PUT'])
@jwt_required()
def update_note(catatan_id):
    note = Catatan.query.get_or_404(catatan_id)
    data = request.json
    note.catatan = data.get('catatan', note.catatan)
    db.session.commit()
    return jsonify({'message': 'Note updated successfully'})

@routes.route('/notes/<int:catatan_id>', methods=['DELETE'])
@jwt_required()
def delete_note(catatan_id):
    note = Catatan.query.get_or_404(catatan_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'})
