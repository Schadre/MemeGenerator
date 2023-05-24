from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Meme, meme_schema, memes_schema


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/memes', methods=['POST'])
@token_required
def create_meme(current_user_token):
    Quote = request.json['Quote']
    Img = request.json['Img']
    user = User.query.get(current_user_token.id)

    meme = Meme(Quote=Quote, Img=Img, user_id=user.id)

    db.session.add(meme)
    db.session.commit()

    response = meme_schema.dump(meme)
    return jsonify(response)

@api.route('/memes', methods=['GET'])
@token_required
def get_memes(current_user_token):
    user_id = current_user_token.id
    memes = Meme.queru.filter_by(user_id=user_id).all()
    response = memes_schema.dump(memes)
    return jsonify(response)

@api.route('/memes/<id>', methods=['GET'])
@token_required
def get_meme(current_user_token, id):
    me = current_user_token.token
    if me == current_user_token.token:
        meme = Meme.query.get(id)
        response = meme_schema.dump(meme)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}), 401


@api.route('/memes/<id>', methods=['POST', 'PUT'])
@token_required
def update_meme(current_user_token, id):
    meme = Meme.query.get(id)
    meme.Quote = request.json['Quote']
    meme.Img = request.json['Img']
    meme.user_id = current_user_token.id

    db.session.commit()
    response = meme_schema.dump(meme)
    return jsonify(response)


@api.route('/memes/<id>', methods=['DELETE'])
@token_required
def delete_meme(current_user_token, id):
    meme = Meme.query.get(id)
    db.session.delete(meme)
    db.session.commit()
    response = meme_schema.dump(meme)
    return jsonify(response)