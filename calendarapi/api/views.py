from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from calendarapi.api.resources import (
    SpecializationListResource,
    AllSpecializationsResource,
    LawyersListResource,
    ScheduleResource,
    AppointmentResource,
    OurTeamResource,
    FeedbackResource,
    NewsResource,
    ContactResource,
    ReviewsResource,
    PossibilitiesResource,
    ClientResource,
    ProBonoResource,
    HeroBlockResource,
)


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(SpecializationListResource, "/lawyer-specs", endpoint="specialization")
api.add_resource(LawyersListResource, "/lawyers", endpoint="lawyers")
api.add_resource(ScheduleResource, "/schedule", endpoint="schedule")
api.add_resource(AppointmentResource, "/appointment", endpoint="appointment")
api.add_resource(OurTeamResource, "/our-team", endpoint="our_team")
api.add_resource(FeedbackResource, "/feedback", endpoint="feedback")
api.add_resource(NewsResource, "/news", endpoint="news")
api.add_resource(ContactResource, "/contacts", endpoint="contacts")
api.add_resource(
    AllSpecializationsResource, "/specializations", endpoint="specializations"
)
api.add_resource(ReviewsResource, "/reviews", endpoint="reviews")
api.add_resource(PossibilitiesResource, "/possibilities", endpoint="possibilities")
api.add_resource(ClientResource, "/clients", endpoint="clients")
api.add_resource(ProBonoResource, "/pro_bono", endpoint="pro_bono")
api.add_resource(HeroBlockResource, "/hero", endpoint="hero")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
