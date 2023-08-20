from flask import Flask
from flask import Flask
from applications.models import db, User
from flask_cors import CORS
from flask_restful import Api
from applications.worker import celery, ContextTask
import os

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'TicketDB.sqlite3')
    app.config['SECRET_KEY'] = "21f100"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir)

    db.init_app(app)
    api = Api(app)
    return app, api


app, api = create_app()
app.app_context().push()

celery=celery
CELERY_BROKER_URL="redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/2"

celery.conf.update(
    broker_url="redis://127.0.0.1:6379/1",
    result_backend="redis://127.0.0.1:6379/2",
    timezone="Asia/Kolkata"
)

celery.Task = ContextTask

# Admin end points
from applications.apiAdmin import *
api.add_resource(AdminResource, "/api/admin/login", "/api/admin/dashboard")
api.add_resource(MovieResource, "/api/admin/movie", "/api/admin/movie/<int:movieId>")
api.add_resource(VenueResource, "/api/admin/venue", "/api/admin/venue/<int:venueId>")
api.add_resource(ShowResource, "/api/admin/show", "/api/admin/show/<int:showId>")
api.add_resource(ExportResource, "/api/admin/export", "/api/admin/export/<int:venueId>")

# User end points
from applications.apiUser import *
api.add_resource(LoginResource, "/api/login", "/api/logout")
api.add_resource(UserResource, "/api/signup", "/api/dashboard")
api.add_resource(SearchRate, "/api/search", "/api/rate")
api.add_resource(BookingResource, "/api/book/<int:showId>", "/api/booked/<int:userId>")


def admin():
  check = User.query.filter_by(is_admin = True).first()
  if check is None:
    admin = User(name="Admin", 
                  email_id="admin_nd@gmail.com", 
                  password="1010", 
                  is_admin=True)
    db.session.add(admin)
    db.session.commit()
  return True

if __name__ == '__main__':
  # Run the Flask app
  db.create_all()
  admin()
  app.run(debug=True)