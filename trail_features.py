# trail_features.py

from flask import abort, make_response
from config import db
from models import Trail, Feature, trail_schema

def link_feature_to_trail(trail_id, feature_id):
    trail = Trail.query.get(trail_id)
    feature = Feature.query.get(feature_id)

    if not trail:
        abort(404, f"Trail with ID {trail_id} not found.")
    if not feature:
        abort(404, f"Feature with ID {feature_id} not found.")

    if feature not in trail.features:
        trail.features.append(feature)
        db.session.commit()

    return trail_schema.dump(trail), 200

def remove_feature_from_trail(trail_id, feature_id):
    trail = Trail.query.get(trail_id)
    feature = Feature.query.get(feature_id)

    if not trail or not feature:
        abort(404, "Trail or Feature not found.")

    if feature in trail.features:
        trail.features.remove(feature)
        db.session.commit()

    return make_response(f"Feature {feature_id} unlinked from Trail {trail_id}.", 200)
