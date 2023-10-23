from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from calendarapi.api.resources import (
    CityListResource,
    SpecializationListResource,
    LawyersListResource,
    ScheduleResource,
    AppointmentResource,
)


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(CityListResource, "/cities", endpoint="cities")
api.add_resource(
    SpecializationListResource, "/specialization", endpoint="specialization"
)
api.add_resource(LawyersListResource, "/lawyers", endpoint="lawyers")
api.add_resource(ScheduleResource, "/schedule", endpoint="schedule")
api.add_resource(AppointmentResource, "/appointment", endpoint="appointment")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
