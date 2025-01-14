# trails.py

from flask import make_response, abort
from config import db
from models import Trail, trails_schema, trail_schema

def read_all():
    trails = Trail.query.all()
    return trails_schema.dump(trails)

def create(trail_data):
    trail_name = trail_data.get("TrailName")
    existing_trail = Trail.query.filter(Trail.TrailName == trail_name).one_or_none()

    if existing_trail is None:
        new_trail = trail_schema.load(trail_data, session=db.session)
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201
    else:
        abort(
            406,
            f"Trail with name {trail_name} already exists",
            )
def read_one(trail_id):
    trail = Trail.query.get(trail_id)
    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(
            404, f"Trail with trailID: {trail_id} not found"
            )

def update(trail_name, trail_data):
    existing_trail = Trail.query.filter(Trail.TrailName == trail_name).one_or_none()
    if existing_trail:
        update_trail = trail_schema.load(trail_data, session=db.session)
        existing_trail.TrailName = update_trail.TrailName
        existing_trail.TrailSummary = update_trail.TrailSummary
        existing_trail.TrailDescription = update_trail.TrailDescription
        existing_trail.Difficulty = update_trail.Difficulty
        existing_trail.Location = update_trail.Location
        existing_trail.Length = update_trail.Length
        existing_trail.ElevationGain = update_trail.ElevationGain
        existing_trail.RouteType = update_trail.RouteType

        db.session.merge(existing_trail)
        db.session.commit()
        return trail_schema.dump(existing_trail), 201
    else:
        abort(
            404,
            f"Trail with name {trail_name} not found"
            )
def delete(trail_name):
    existing_trail = Trail.query.filter(Trail.TrailName == trail_name).one_or_none()
    if existing_trail:
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(
            f"{trail_name} successfully deleted", 200
            )
    else:
        abort(
            404,
            f"Trail with name {trail_name} not found"
            )
