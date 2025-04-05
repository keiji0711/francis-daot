from flask import Flask
from routes.main import bp as main_bp
from routes.staff import bp as staff_bp
from routes.auth import bp as auth_bp

app = Flask(__name__)

app.secret_key = "12345"


app.register_blueprint(main_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
