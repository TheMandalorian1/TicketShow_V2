from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime

# Database instance
db = SQLAlchemy()

class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email_id = Column(String(50), nullable=False)
    password = Column(String(15), nullable=False)
    is_admin = Column(String, default=False, nullable=False)
    latest_log = Column(String(), default = datetime.now(), nullable=False)
    books = relationship("Register", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email_id='{self.email_id}')"

class Movie(db.Model):
    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String(50), nullable=False)
    picture = Column(String, nullable=False)
    description = Column(String(100), nullable=False)
    movie_rating = Column(Float, default=0)
    num_ratings = Column(Integer, default=0)
    shows = relationship("Show", back_populates="movie", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Movie(movie_id={self.movie_id}, movie_name='{self.movie_name}')"
   

class Venue(db.Model):
    venue_id = Column(Integer, primary_key=True, autoincrement=True)
    venue_name = Column(String(50), nullable=False)
    venue_location = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    shows = relationship("Show", back_populates="venue", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Venue(venue_id={self.venue_id}, venue_name='{self.venue_name}')"
    
class Show(db.Model):
    show_id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_price = Column(Integer, nullable=False)
    ticket_booked = Column(Integer, nullable=False, default=0)
    start = Column(String, nullable=False)
    end = Column(String, nullable=False)
    movie_name = Column(String, nullable=False)
    venue_name = Column(String, nullable=False)
    movie_rating = Column(Float, nullable=False)
    total_capacity = Column(Integer, nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.movie_id", ondelete="CASCADE"), nullable=False)
    venue_id = Column(Integer, ForeignKey("venue.venue_id", ondelete="CASCADE"), nullable=False)
    venue = relationship("Venue", back_populates="shows",)
    movie = relationship("Movie", back_populates="shows",)
    books = relationship("Register", back_populates="shows", cascade="all, delete-orphan") 

    def __repr__(self):
        return f"Show(show_id={self.show_id}, ticket_price={self.ticket_price})"

class Register(db.Model):
    register_id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_count = Column(Integer, nullable=False)
    show_id = Column(Integer, ForeignKey("show.show_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="books")
    shows = relationship("Show", back_populates="books")

    def __repr__(self):
        return f"Register(register_id={self.register_id}, ticket_count={self.ticket_count})"