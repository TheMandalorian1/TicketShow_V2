from flask import request, session
from flask_restful import Resource, marshal
from applications.models import *
from applications.security import user_token_required
from sqlalchemy import func
from applications.store import token_genrator
from applications.store import movie_fields, show_fields
from applications.store import login_parser, signup_parser, rating_parser, booking_parser
from flask_caching import Cache
from flask import current_app as app

app.config["CACHE_TYPE"] = "redis"
app.config['CACHE_REDIS_HOST'] = "localhost"
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379"  
app.config['CACHE_DEFAULT_TIMEOUT'] = 500
cache = Cache(app)

class UserResource(Resource):
    @user_token_required
    @cache.cached(timeout=300)
    def get(self):
        movies = Movie.query.all()
        shows = Show.query.all()
        shows_, movies_ = [], []

        for v in shows:
            shows_.append(marshal(v, show_fields))

        for m in movies:
            movies_.append(marshal(m, movie_fields))

        return {'message': "Logged in successfully.",
                'shows': shows_,
                'movies': movies_
                }, 200


    def post(self):
        data = signup_parser.parse_args()

        check_user = User.query.filter_by(email_id=data.get('email')).first()

        if check_user is None:
            new_user = User(
                name=data.get('name').strip(),
                email_id=data.get('email').strip(),
                password=data.get('password').strip())

            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(email_id=data.get('email')).first()
            session['uid'] = user.id
            return {'message': 'User created successfully!',
                    'token': token_genrator(user),
                    'name': user.name,
                    'uid': user.id
                    }, 200
        return {'error': 'Token is not passed!'}
    
class LoginResource(Resource):
    def get(self):
        session.clear()
        cache.clear()
        return 200

    def post(self):
        data = login_parser.parse_args()

        user = User.query.filter_by(email_id=data.get('email'), is_admin=False).first()

        if user is not None:
            if user.password == data.get('password'):
                user.latest_log = datetime.now()
                db.session.commit()
                session['uid'] = user.id
                return {"message": "User login successful.",
                        'token': token_genrator(user),
                        'name': user.name,
                        'uid': user.id
                        }, 200
            return {'error': "Incorrect password. Please try again!"}
        return {'error': "Email doesn't exists!"}
    

class SearchRate(Resource):
    @user_token_required
    def get(self):
        query = request.args
        if 'mid' in query:
            filtered = Show.query.filter(func.lower(Show.movie_id) == query.get('mid').lower()).all()
        else:
            qstr = query.get('q')
            db_query = f'%{qstr}%'
            filtered = Show.query.filter(
                (func.lower(Show.movie_name).like(db_query)) |
                (func.lower(Show.venue_name).like(db_query)) |
                ( Show.movie_rating == query.get('q') )
            ).all()
        filtered_ = []    
        for show in filtered:
            filtered_.append(marshal(show, show_fields))
        return {'matched_shows': filtered_}, 200
    
    @user_token_required
    def post(self):
        movieId = request.args.get('mid')
        # Check if the movie exists
        movie_query = Movie.query.filter_by(movie_id=movieId).first()

        if movie_query:
            data = rating_parser.parse_args().get('points')
            total_points = movie_query.movie_rating * movie_query.num_ratings
            total_points += float(data)
            movie_query.num_ratings += 1
            movie_query.movie_rating = round(total_points / movie_query.num_ratings, 1)
            for s in movie_query.shows:
                s.movie_rating = round(total_points / movie_query.num_ratings, 1)

            db.session.commit()  
            cache.clear()
            return {'message': 'Thankyou for rating!'}, 200
        return {'message': 'Movie not found'}, 404

class BookingResource(Resource):
    @user_token_required
    def get(self, userId):
        shows = Register.query.filter_by(user_id = userId).all()
        shows_, tickets = [], {}
        for s in shows:
            show_query = Show.query.filter_by(show_id=s.show_id).first()
            shows_.append(marshal(show_query, show_fields))
            tickets[s.show_id] = (s.ticket_count)
        return {'shows': shows_,
                'tickets': tickets}, 200
    

    @user_token_required
    def post(self, showId):
        show_query = Show.query.filter_by(show_id=showId).first()
        
        if show_query:
            data = booking_parser.parse_args()
            rem_seats = show_query.total_capacity - show_query.ticket_booked
            if rem_seats >= int(data.get('no_of_tickets')): 
                new_booking = Register(
                    ticket_count = int(data.get('no_of_tickets')),
                    show_id = showId,
                    user_id = int(data.get('uid'))
                )
                show_query.ticket_booked = show_query.ticket_booked + int(data.get('no_of_tickets'))
                db.session.add(new_booking)
                db.session.commit()
                cache.clear()
                return {'message': 'Thankyou! Enjoy your movie!'},200
            return {'error': 'Oops! Show is Housefull.'}, 409
        return {'error': 'Show not found'}, 404       
