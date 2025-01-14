# features.py

from flask import abort, make_response
from config import db
from models import Feature, feature_schema, features_schema

def read_all():
    feature_list = Feature.query.all()
    return features_schema.dump(feature_list)

def read_one(feature_id):
    feature = Feature.query.get(feature_id)

    if feature is not None:
        return feature_schema.dump(feature)
    else:
        abort(
            404, f"Feature with ID {feature_id} not found"
            )
        
def update(feature_id, feature_data):
    existing_feature = Feature.query.get(feature_id)

    if existing_feature:
        update_feature = feature_schema.load(feature_data, session=db.session)
        existing_feature.TrailFeature = update_feature.TrailFeature
        db.session.merge(existing_feature)
        db.session.commit()
        return feature_schema.dump(existing_feature), 201
    else:
        abort(404, f"Feature ID {feature_id} not found")

def delete(feature_id):
    existing_feature = Feature.query.get(feature_id)

    if existing_feature:
        db.session.delete(existing_feature)
        db.session.commit()
        return make_response(f"Feature {feature_id} successfully deleted", 204)
    else:
        abort(404, f"Feature with ID {feature_id} not found")

def create (feature_data):
    data = feature_data.get("TrailFeature")
    existing_feature = Feature.query.filter(Feature.TrailFeature == data).one_or_none()

    if existing_feature is None:
        new_feature = feature_schema.load(feature_data, session=db.session)
        db.session.add(new_feature)
        db.session.commit()
        return feature_schema.dump(new_feature), 201
    else:
        abort(
            404,
            f"Feature {data} already exists"
            )
                        
