# models.py
from datetime import datetime
import pytz
from marshmallow_sqlalchemy import fields
from config import db, ma

TrailFeatureTable = db.Table (
    "TrailFeature",
    db.metadata,
    db.Column("TrailID", db.Integer, db.ForeignKey("CW2.Trail.TrailID"), primary_key=True),
    db.Column("TrailFeatureID", db.Integer, db.ForeignKey("CW2.Feature.TrailFeatureID"), primary_key=True),
    schema="CW2"
    )

class Trail(db.Model):
    __tablename__ = "Trail"
    __table_args__ = {"schema": "CW2"}
    
    TrailID = db.Column(db.Integer, primary_key=True, autoincrement=False)
    TrailName = db.Column(db.String(50), nullable=False)
    TrailSummary = db.Column(db.String(100))
    TrailDescription = db.Column(db.Text)
    Difficulty = db.Column(db.String(10))
    Location = db.Column(db.String(50))
    Length = db.Column(db.Float)
    ElevationGain = db.Column(db.Float)
    RouteType = db.Column(db.String(20))

    features = db.relationship(
        "Feature",
        secondary = TrailFeatureTable,
        back_populates="trails"
        )
class Feature(db.Model):
    __tablename__ = "Feature"
    __table_args__ = {"schema": "CW2"}

    TrailFeatureID = db.Column(db.Integer, primary_key=True, autoincrement=False)
    TrailFeature = db.Column(db.String(75), nullable=False)
    trails = db.relationship(
        "Trail",
        secondary = TrailFeatureTable,
        back_populates =  "features"
        )
class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sqla_session = db.session
        include_fk = True

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        include_relationships = True

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
