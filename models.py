# models.py

from datetime import datetime
from config import db, ma

class Media(db.Model):
    __tablename__ = "media"
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(96))
    IsMovie = db.Column(db.Boolean)
    SeriesTitle = db.Column(db.String(96))
    Season = db.Column(db.Integer)
    Episode = db.Column(db.Integer)
    Source = db.Column(db.String(96))
    DateViewed = db.Column(db.DateTime, default=datetime.now(datetime.UTC))
    PersonalRating = db.Column(db.Integer)
    RatingSource = db.Column(db.String(96)
    RatingValue = db.Column(db.float)

class MediaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Media
        load_instance = True
        sqla_session = db.session

one_media_scheme = MediaSchema()
all_media_scheme = MediaSchema(many=True)    
    