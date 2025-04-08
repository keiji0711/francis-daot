from flask import Flask
from routes.main import bp as main_bp
from routes.staff import bp as staff_bp
from routes.auth import bp as auth_bp
from routes.deletee_routes import bp as deletee_bp
from routes.adding_routes import bp as adding_bp
from routes.update_routes import bp as update_bp

app = Flask(__name__)

app.secret_key = "12345"


app.register_blueprint(main_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(deletee_bp)
app.register_blueprint(adding_bp)
app.register_blueprint(update_bp)

if __name__ == '__main__':
    app.run(debug=True)
