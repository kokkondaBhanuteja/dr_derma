import os
from app import create_app

# Create app instance
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000),debug = True)
