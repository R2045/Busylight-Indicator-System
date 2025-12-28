from flask import send_from_directory
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
