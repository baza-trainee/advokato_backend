from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from calendarapi.api.resources import (
    UserResource,
    UserList,
    CityListResource,
    SpecializationListResource,
    LawyerResource,
    LawyersListResource,
    CityResource,
)


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(CityListResource, "/cities", endpoint="cities")
api.add_resource(CityResource, "/city/<int:city_id>", endpoint="city_by_id")
api.add_resource(
    SpecializationListResource, "/specialization", endpoint="specialization"
)
api.add_resource(LawyerResource, "/lawyer/<int:lawyer_id>", endpoint="lawyer_by_id")
api.add_resource(LawyersListResource, "/lawyers", endpoint="lawyers")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
