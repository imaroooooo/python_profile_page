# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Configure application settings
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for session management and flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profile.db'  # SQLite database path
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Directory for storing uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum file upload size (16MB)

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Define Profile model for storing lecturer's information
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Lecturer's full name
    title = db.Column(db.String(200))  # Professional title/position
    bio = db.Column(db.Text)  # Professional biography
    profile_picture = db.Column(db.String(200))  # Path to profile picture
    background_image = db.Column(db.String(200))  # Path to background image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of profile creation

# Define PortfolioItem model for storing portfolio entries
class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Title of the portfolio item
    description = db.Column(db.Text)  # Detailed description of the item
    image = db.Column(db.String(200))  # Path to the portfolio item image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of item creation

# Create database tables
with app.app_context():
    db.create_all()

# Define allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main profile page"""
    # Get the profile and portfolio items from the database
    profile = Profile.query.first()
    portfolio_items = PortfolioItem.query.order_by(PortfolioItem.created_at.desc()).all()
    return render_template('index.html', profile=profile, portfolio_items=portfolio_items)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """Handle profile editing and updates"""
    # Get existing profile or create a new one if none exists
    profile = Profile.query.first()
    if not profile:
        profile = Profile(name="Your Name", title="Your Title")
        db.session.add(profile)
        db.session.commit()

    if request.method == 'POST':
        # Update profile information from form data
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

        # Save changes to database
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('index'))

    return render_template('edit_profile.html', profile=profile)

@app.route('/add_portfolio', methods=['GET', 'POST'])
def add_portfolio():
    """Handle adding new portfolio items"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        
        # Handle portfolio image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                # Create new portfolio item
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
    # Run the application in debug mode
    app.run(debug=True) 