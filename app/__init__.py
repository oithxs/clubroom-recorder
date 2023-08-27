from app.core import app
from app.routes.register import blueprint as register_blueprint
from app.routes.login import blueprint as login_blueprint


app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)
