import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=5005, host='0.0.0.0', debug=True)  # 5005 is rarely used by system