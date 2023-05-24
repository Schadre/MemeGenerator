from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, Response
from helpers import token_required
from models import db, User, Meme, meme_schema, memes_schema
from flask_login import current_user, login_required

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route("/")
def home():
    return render_template("index.html")

@site.route("/profile")
def profile():
    return render_template("profile.html")

@site.route("/Memes")
@login_required
def Memes():
    memes = Meme.query.all()
    return render_template("Memes.html", memes=memes)

@site.route('/add_meme', methods=['POST'])
@login_required
def add_meme():
    quote = request.form['Quote']
    img = request.files['Img']
    user_token = current_user.token

    if len(quote) > 15:
        flash('Maximum 15 characters allowed for the quote.')
        return redirect(url_for(add_meme))

    if not quote or not img:
        flash('Please provide both a quote and an image', 'error')
        return redirect(url_for('site.Memes'))
    
    image_data = img.read()

    meme = Meme(quote=quote, img=image_data, user_token=user_token)
    db.session.add(meme)
    db.session.commit()

    flash('Meme added successfully', 'success')
    return redirect(url_for('site.Memes'))
    
    return redirect(url_for('site.Memes'))

@site.route('/delete_meme/<id>', methods=['POST'])
@login_required
def delete_meme(id):
    meme = Meme.query.get(id)
    if meme:
        if meme.user_token == current_user.token:
            db.session.delete(meme)
            db.session.commit()
            flash('Meme deleted successfully', 'success')
            return redirect(url_for('site.Memes'))
        else: 
            flash('You do not have permission to delete this Meme.', 'error')
    else:
        flash('Meme not found', 'error')

    return redirect(url_for('site.Memes'))

@site.route('/download_meme/<id>', methods=['GET'])
@login_required
def download_meme(id):
    meme = Meme.query.get(id)
    if meme:
        headers = {
            'Content-Type': 'image/jpeg',
            'Content-Disposition': f'attachment; filename={id}.jpg'
        }

        return Response(meme.img, headers=headers)
    else:
        flash('Meme not found', 'error')
        return redirect(url_for('site.Memes'))

@site.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    first = request.form['first']
    last = request.form['last']
    username = request.form['username']
    email = request.form['email']

    current_user.first = first
    current_user.last = last
    current_user.username = username 
    current_user.email = email

    db.session.commit()

    flash('Profile updated successfully', 'success')
    return redirect(url_for('site.profile'))

@site.errorhandler(400)
@site.errorhandler(401)
@site.errorhandler(403)
@site.errorhandler(404)
@site.errorhandler(500)
def error_handler(error):
    error_code = error.code
    error_message = error.description
    return render_template('Error.html', error_code=error_code, error_message=error_message), error_code