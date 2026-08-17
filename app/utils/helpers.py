"""
Helper functions
"""
import os
from werkzeug.utils import secure_filename
from datetime import datetime


def save_uploaded_file(file, folder, user_id=None):
    """Save uploaded file and return relative path"""
    if not file:
        return None
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if user_id:
        filename = f"{user_id}_{timestamp}_{filename}"
    else:
        filename = f"{timestamp}_{filename}"
    
    filepath = os.path.join(folder, filename)
    file.save(filepath)
    
    # Return relative path for database
    return filepath.replace('app/static/', '')


def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
