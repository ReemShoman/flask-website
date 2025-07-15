import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join('static', 'pics', secure_filename(filename))
    file.save(path)

    # Resize image
    try:
        img = Image.open(path)
        img.thumbnail((500, 500))  # Resize to max 500x500
        img.save(path)
    except Exception as e:
        print("Error resizing image:", e)

    return filename
