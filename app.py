from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profile.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200))
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(200))
    background_image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    profile = Profile.query.first()
    portfolio_items = PortfolioItem.query.order_by(PortfolioItem.created_at.desc()).all()
    return render_template('index.html', profile=profile, portfolio_items=portfolio_items)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    profile = Profile.query.first()
    if not profile:
        profile = Profile(name="Your Name", title="Your Title")
        db.session.add(profile)
        db.session.commit()

    if request.method == 'POST':
        profile.name = request.form.get('name')
        profile.title = request.form.get('title')
        profile.bio = request.form.get('bio')

        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile.profile_picture = filename

        # Handle background image upload
        if 'background_image' in request.files:
            file = request.files['background_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile.background_image = filename

        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('index'))

    return render_template('edit_profile.html', profile=profile)

@app.route('/add_portfolio', methods=['GET', 'POST'])
def add_portfolio():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                portfolio_item = PortfolioItem(
                    title=title,
                    description=description,
                    image=filename
                )
                db.session.add(portfolio_item)
                db.session.commit()
                flash('Portfolio item added successfully!')
                return redirect(url_for('index'))

    return render_template('add_portfolio.html')

if __name__ == '__main__':
    app.run(debug=True) 