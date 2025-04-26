# University Lecturer Profile

A modern web application for university lecturers to showcase their profile, background, and portfolio.

## Features

- Profile picture and background image upload
- Professional bio and title management
- Portfolio management with images and descriptions
- Modern, responsive design
- User-friendly interface

## Setup Instructions

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. First, visit the "Edit Profile" page to set up your basic information
2. Upload your profile picture and background image
3. Add your professional bio
4. Use the "Add Portfolio" page to showcase your work
5. All changes will be immediately visible on your profile page

## File Structure

- `app.py` - Main application file
- `templates/` - HTML templates
  - `base.html` - Base template with common elements
  - `index.html` - Main profile page
  - `edit_profile.html` - Profile editing form
  - `add_portfolio.html` - Portfolio item creation form
- `static/` - Static files (CSS, uploaded images)
  - `uploads/` - Directory for uploaded images

## Security Notes

- The application uses a SQLite database for simplicity
- File uploads are restricted to image files only
- Maximum file size is limited to 16MB
- Remember to change the SECRET_KEY in production 