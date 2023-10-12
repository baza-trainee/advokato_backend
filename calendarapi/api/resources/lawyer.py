from typing import List

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from calendarapi.api.schemas import LawyerSchema
from calendarapi.extensions import db, ma
from calendarapi.models import Lawyer, Specialization


class LawyersListResource(Resource):
    """
    Lawyers List Resource

    ---
    get:
      tags:
        - Lawyer
      summary: Get a list of lawyers.
      description: Get a list of lawyers.
      responses:
        200:
          description: List of lawyers
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/LawyerSchema'
        404:
          description: No lawyers found.
    post:
      tags:
        - Lawyer
      summary: Create a new lawyer.
      description: Create a new lawyer.
      requestBody:
        required: true
        content:
          application/json:
              schema:
                  $ref: '#/components/schemas/LawyerSchema'
      responses:
        201:
          description: Lawyer created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LawyerSchema'
        400:
          description: Bad request, validation error in lawyer data
    """

    lawyer_schema: LawyerSchema = LawyerSchema()

    def get(self):
        lawyers: List[Lawyer] = (
            db.session.query(Lawyer).options(joinedload(Lawyer.specializations)).all()
        )
        return self.lawyer_schema.dump(lawyers, many=True), 200

    @jwt_required()
    def post(self):
        try:
            lawyer: Lawyer = self.lawyer_schema.load(request.json)
        except ma.ValidationError as e:
            return {"message": str(e)}, 400

        lawyer_mail: str = lawyer.lawyer_mail
        specialization_names: List[Specialization] = lawyer.specializations
        existing_lawyer: Lawyer = (
            db.session.query(Lawyer).filter_by(lawyer_mail=lawyer_mail).first()
        )
        if existing_lawyer:
            return {"message": "Lawyer with this email already exists"}, 400

        specializations: List[Specialization] = []
        new_spec_for_db: List[Specialization] = []

        for specialization in specialization_names:
            spec_name: str = specialization.specialization_name
            specialization: Specialization = (
                db.session.query(Specialization)
                .filter_by(specialization_name=spec_name)
                .first()
            )

            if not specialization:
                specialization = Specialization(specialization_name=spec_name)
                new_spec_for_db.append(specialization)
                specializations.append(specialization)
            else:
                specializations.append(specialization)
        lawyer.specializations = specializations

        try:
            db.session.add_all([lawyer, *new_spec_for_db])
            db.session.commit()
            return {"message": "Lawyer created successfully"}, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Error creating lawyer"}, 500


class LawyerResource(Resource):
    """
    Lawyer Resource

    ---
    patch:
      tags:
        - Lawyer
      summary: Update a lawyer.
      description: Update a lawyer with the specified ID.
      parameters:
        - in: path
          name: lawyer_id
          schema:
            type: integer
          required: true
          description: ID of the lawyer to update.
      requestBody:
        required: true
        content:
          application/json:
              schema:
                $ref: '#/components/schemas/LawyerSchema'
      responses:
        200:
          description: Lawyer updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LawyerSchema'
        400:
          description: Bad request, validation error in lawyer data
        404:
          description: Lawyer not found

    delete:
      tags:
        - Lawyer
      summary: Delete a lawyer.
      description: Delete a lawyer with the specified ID.
      parameters:
        - in: path
          name: lawyer_id
          schema:
            type: integer
          required: true
          description: ID of the lawyer to delete.
      responses:
        204:
          description: Lawyer deleted successfully
        400:
          description: Bad request, validation error
        404:
          description: Lawyer not found
    """

    lawyer_schema: LawyerSchema = LawyerSchema()

    @jwt_required()
    def patch(self, lawyer_id: int):
        lawyer: Lawyer = (
            db.session.query(Lawyer)
            .filter_by(id=lawyer_id)
            .options(joinedload(Lawyer.specializations))
            .first()
        )
        if lawyer is None:
            return {"message": "Lawyer not found"}, 404

        try:
            lawyer: Lawyer = self.lawyer_schema.load(
                request.json, instance=lawyer, partial=True, session=db.session
            )
        except ma.ValidationError as e:
            return {"message": str(e)}, 400

        db.session.add(lawyer)
        db.session.commit()
        return self.lawyer_schema.dump(lawyer), 200

    @jwt_required()
    def delete(self, lawyer_id: int):
        lawyer: Lawyer = (
            db.session.query(Lawyer)
            .filter_by(id=lawyer_id)
            .options(joinedload(Lawyer.specializations))
            .first()
        )
        if lawyer is None:
            return {"message": "Lawyer not found"}, 404
        try:
            db.session.delete(lawyer)
            db.session.commit()
            return "", 204
        except IntegrityError as e:
            return {"message": str(e)}, 400
