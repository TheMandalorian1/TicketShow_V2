from flask import request, session
from flask_restful import Resource, marshal
from applications.models import *
from applications.security import admin_token_required
from applications.task import exporter
from applications.apiUser import cache
from flask import current_app as app
from applications.store import token_genrator,poster_saver, poster_remover
from applications.store import movie_fields, venue_fields, show_fields
from applications.store import login_parser, venue_parser, show_parser


class AdminResource(Resource):
    @admin_token_required
    def get(self):
        movies = Movie.query.all()
        venues = Venue.query.all()
        venues_, movies_ = [], []

        for v in venues:
            venues_.append(marshal(v, venue_fields))

        for m in movies:
            movies_.append(marshal(m, movie_fields))

        return {'message': "Logged in successfully.",
                'venues': venues_,
                'movies': movies_
                }, 200

    def post(self):
        data = login_parser.parse_args()

        admin = User.query.filter_by(
            email_id=data["email"], is_admin=True).first()

        if admin is not None:
            if admin.password == data['password']:
                return {"message": "Admin login successful.",
                        'token': token_genrator(admin)
                        }, 200
            return {'error': "Incorrect password. Please try again!"}
        return {'error': "Email doesn't match!"}

class MovieResource(Resource):
    def get(self, movieId):
        # Check if the movie exists
        movie_query = Movie.query.filter_by(movie_id=movieId).first()

        if movie_query:
            return marshal(movie_query, movie_fields), 200
        return {'message': 'Movie not found'}, 404

    @admin_token_required
    def post(self):
        data = request.form
        # Check if the movie already exists
        movie_query = Movie.query.filter_by(
            movie_name=data.get('movie_name')).first()

        if movie_query is None:
            picture = poster_saver(request.files.get('poster'))
            new_movie = Movie(
                movie_name=data.get('movie_name'),
                description=data.get('description'),
                movie_rating=data.get('movie_rating'),
                num_ratings = 1,
                picture=picture)

            db.session.add(new_movie)
            db.session.commit()
            cache.clear()
            return {'message': 'Movie added successfully.'}, 201
        return {'error': "Movie already exists!"}

    @admin_token_required
    def put(self, movieId):
        data = request.form

        # Check if the movie exists
        movie_query = Movie.query.filter_by(movie_id=movieId).first()

        if movie_query:
            movie_query.movie_name = data['movie_name']
            movie_query.description = data['description']

            for s in movie_query.shows:
                s.movie_name = data.get('movie_name')  

            # check if image is updated
            if request.files.get('poster'):
                picture = poster_saver(request.files.get('poster'))
                poster_remover(movie_query.picture)

                movie_query.picture = picture

            db.session.commit()
            cache.clear()
            return {'message': 'Movie updated successfully.'}, 200
        return {'error': "Movie doesn't exists!"}, 404

    @admin_token_required
    def delete(self, movieId):
        # Check if the movie exists
        movie_query = Movie.query.filter_by(movie_id=movieId).first()

        if movie_query:
            data = request.get_json()
            confirmation = data.get('confirm', False)

            if confirmation:
                # Remove the movie from the database
                db.session.delete(movie_query)

                # Remove the associated poster
                poster_remover(movie_query.picture)

                db.session.commit()
                cache.clear()
                return {'message': 'Movie deleted successfully.'}, 200
            return {'error': "Deletion not confirmed!"}
        return {'error': "Movie doesn't exists!"}


class VenueResource(Resource):
    def get(self, venueId):
        # Check if the venue exists
        venue_query = Venue.query.filter_by(venue_id=venueId).first()

        if venue_query:
            return marshal(venue_query, venue_fields), 200
        
        return {'error': "Venue doesn't exists!"}, 404

    @admin_token_required
    def post(self):
        data = venue_parser.parse_args()

        # Check if the new venue details already exists
        venue_exists = Venue.query.filter_by(venue_name=data['venue_name'],
                                             venue_location=data['address']).first()

        if venue_exists:
            return {'error': "Venue already exists!"}, 409
        else:
            new_venue = Venue(
                venue_name=data['venue_name'],
                venue_location=data['address'],
                capacity=data['capacity']
            )

        db.session.add(new_venue)
        db.session.commit()
        cache.clear()
        return {'message': 'Venue added successfully.'}, 201

    @admin_token_required
    def put(self, venueId):
        data = venue_parser.parse_args()

        # Check if the venue exists
        venue_query = Venue.query.filter_by(venue_id=venueId).first()
        if venue_query:
            # Check if the new venue details already exists
            venue_exists = Venue.query.filter_by(venue_name=data['venue_name'],
                                                 venue_location=data['address']).first()
            if venue_exists and venue_exists.venue_id != venueId:
                return {'message': 'Venue already exists'}, 409

            else:
                venue_query.venue_name = data.get('venue_name')
                venue_query.venue_location = data.get('address')
                venue_query.capacity = data.get('capacity')
                for s in venue_query.shows:
                    s.total_capacity = data.get('capacity')
                    s.venue_name = data.get('venue_name') + ", " + data.get('address')

                db.session.commit()
                cache.clear()
                return {'message': 'Venue updated successfully.'}, 200
        return {'error': 'Venue not found!'}, 404

    @admin_token_required
    def delete(self, venueId):
        # Check if the venue exists
        venue_query = Venue.query.filter_by(venue_id=venueId).first()

        if venue_query:
            data = request.get_json()
            confirmation = data.get('confirm', False)

            if confirmation:
                db.session.delete(venue_query)
                db.session.commit()
                cache.clear()
                return {'message': 'Venue deleted successfully.'}, 200

            return {'error': "Deletion not confirmed!"}, 400
        return {'error': 'Venue not found!'}, 404


class ShowResource(Resource):
    def get(self, showId):
        show_query = Show.query.filter_by(show_id=showId).first()

        if show_query:
            return marshal(show_query, show_fields), 200
        return {'error': 'Show not found'}, 404

    @admin_token_required
    def post(self):
        data = show_parser.parse_args()

        venue_query = Venue.query.filter_by(venue_id=data['venue_id']).first()
        if not venue_query:
            return {'error': 'Venue not found'}, 404

        movie_query = Movie.query.filter_by(movie_id=data['movie_id']).first()
        if not movie_query:
            return {'error': 'Movie not found'}, 404

        new_show = Show(
            movie_id=movie_query.movie_id,
            venue_id=venue_query.venue_id,
            ticket_price=data['ticket_price'],
            start=data['start'],
            end=data['end'],
            venue_name=venue_query.venue_name + ", " + venue_query.venue_location,
            movie_name=movie_query.movie_name,
            movie_rating=movie_query.movie_rating,
            total_capacity=venue_query.capacity
        )
        db.session.add(new_show)
        db.session.commit()
        cache.clear()
        return {'message': 'Show added successfully.'}, 201

    @admin_token_required
    def put(self, showId):
        data = show_parser.parse_args()

        show_query = Show.query.filter_by(show_id=showId).first()
        if show_query:
            venue_query = Venue.query.filter_by(venue_id=data['venue_id']).first()
            if venue_query:
                movie_query = Movie.query.filter_by(movie_id=data['movie_id']).first()
                if movie_query:
                    show_query.movie_id=movie_query.movie_id
                    show_query.venue_id=venue_query.venue_id
                    show_query.ticket_price=int(data.get('ticket_price'))
                    show_query.available=venue_query.capacity
                    show_query.start=data.get('start')
                    show_query.end=data.get('end')
                    show_query.venue_name=venue_query.venue_name + ", " + venue_query.venue_location
                    show_query.movie_name=movie_query.movie_name
                    show_query.movie_rating=movie_query.movie_rating
                    show_query.total_capacity=venue_query.capacity

                    db.session.commit()
                    cache.clear()
                    return {'message': 'Show updated successfully.'}, 200
                return {'error': 'Movie not found!'}, 404
            return {'error': 'Show not found!'}, 404
        return {'error': 'Venue not found!'}, 404

    @admin_token_required
    def delete(self, showId):
        show_query = Show.query.filter_by(show_id=showId).first()

        if not show_query:
            return {'error': 'Show not found'}, 404

        if show_query:
            data = request.get_json()
            confirmation = data.get('confirm', False)

            if confirmation:
                db.session.delete(show_query)
                db.session.commit()
                cache.clear()
                return {'message': 'Show deleted successfully.'}, 200

            return {'error': "Deletion not confirmed!"}, 400
        return {'error': 'Show not found!'}, 404


class ExportResource(Resource):
    @admin_token_required
    def get(self):
        venues = Venue.query.all()
        venues_= []
        for v in venues:
            venues_.append(marshal(v, venue_fields))
        return {'venues': venues_}, 200
    

    @admin_token_required
    def post(self, venueId):
        venue_query = Venue.query.filter_by(venue_id = venueId).first()
        shows_det = []
        if venue_query:
            venue_det = [[venue_query.venue_name, venue_query.venue_location, venue_query.capacity]]
            for s in venue_query.shows:
                shows_det.append([s.movie_name, s.start, s.end, s.ticket_price, s.movie_rating, s.ticket_booked])

            exporter(venue_det, shows_det, "admin_nd@gmail.com", "Admin")
            return {'message': 'Venue details sent to your mail.'}, 200
        return {'error': 'Venue not found'}, 404  