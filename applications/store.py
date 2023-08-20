import jwt
import os
from datetime import datetime, timedelta
import secrets
from PIL import Image
from flask import current_app as app
from flask_restful import reqparse, fields
from jinja2 import Template 
from weasyprint import HTML

def poster_saver(poster_file):
    hex_poster_name = secrets.token_hex(5)
    poster, poster_extension = os.path.splitext(poster_file.filename)
    poster_name = hex_poster_name + poster_extension
    poster_path = os.path.join(
        app.config['UPLOAD_FOLDER'], f'src/images/{poster_name}')

    poster_file.save(poster_path)
    output_size = (300, 200)
    resized = Image.open(poster_path)
    resized.thumbnail(output_size)
    resized.save(poster_path)
    return poster_name


def poster_remover(poster_name):
    poster_path = os.path.join(
        app.config['UPLOAD_FOLDER'], f'src/images/{poster_name}')
    if os.path.exists(poster_path):
        os.remove(poster_path)


def token_genrator(user):
    payload = {
        'user_id': user.id,
        'is_admin': user.is_admin,
        'exp': datetime.utcnow() + timedelta(hours=6)  # Token expiration time
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return token

def convertToPDF(htmlContent, pdfFile):
    HTML(string=htmlContent).write_pdf(pdfFile)

def reportGenrator(templateFile, data, username):
    with open(templateFile) as fileTemp:
        template = Template(fileTemp.read())
        html_report = template.render(lister=data, username=username)
        pdf_report = f"src/{username}_MR.pdf"
        convertToPDF(html_report, pdf_report)
        return pdf_report
    
# input parser for login
login_parser = reqparse.RequestParser()
login_parser.add_argument('email', required=True)
login_parser.add_argument('password', required=True)

# input parser for signup
signup_parser = reqparse.RequestParser()
signup_parser.add_argument('name', required=True)
signup_parser.add_argument('email', required=True)
signup_parser.add_argument('password', required=True)

# input parser for venue
venue_parser = reqparse.RequestParser()
venue_parser.add_argument('venue_name', required=True)
venue_parser.add_argument('address', required=True)
venue_parser.add_argument('capacity', required=True)

# input parser for show
show_parser = reqparse.RequestParser()
show_parser.add_argument('movie_id', required=True)
show_parser.add_argument('venue_id', required=True)
show_parser.add_argument('start', required=True)
show_parser.add_argument('end', required=True)
show_parser.add_argument('ticket_price', required=True)

# input parser for movie rating
rating_parser = reqparse.RequestParser()
rating_parser.add_argument('points', required=True)

# input parser for ticket booking 
booking_parser = reqparse.RequestParser()
booking_parser.add_argument('no_of_tickets', required=True)
booking_parser.add_argument('uid', required=True)

# input parser for venue export 
export_parser = reqparse.RequestParser()
export_parser.add_argument('venue_id', required=True)
export_parser.add_argument('user_id', required=True)


# show field parser
show_fields = {
    'show_id': fields.Integer,
    'start': fields.String,
    'end': fields.String,
    'ticket_booked': fields.Integer,
    'ticket_price': fields.Integer,
    'movie_id': fields.Integer,
    'venue_id': fields.Integer,
    'movie_name': fields.String,
    'venue_name': fields.String,
    'movie_rating': fields.Float,
    'total_capacity': fields.Integer,
}

# venue field parser
venue_fields = {
    'venue_id': fields.Integer,
    'venue_name': fields.String,
    'venue_location': fields.String,
    'capacity': fields.Integer,
    'shows': fields.List(fields.Nested(show_fields))
}

# movie field parser
movie_fields = {
    'movie_id': fields.Integer,
    'movie_name': fields.String,
    'picture': fields.String,
    'description': fields.String,
    'movie_rating': fields.Float,
    'shows': fields.List(fields.Nested(show_fields))
}