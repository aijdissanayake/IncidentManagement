import json
from flask import Flask, jsonify

from flask_restful import reqparse, abort, Api, Resource, request, fields, marshal_with

from ..service.incident import save_new_incident, get_all_incidents, get_a_incident, update_a_incident, delete_a_incident

from .. import api

incident_fields = {
    
    'id' : fields.Integer,
    'token' : fields.String(1024),
    'election_id' : fields.Integer,
    'police_station_id' : fields.Integer,
    'polling_station_id' : fields.Integer,
    'reporter_id' : fields.Integer,
    'location' : fields.String(4096),
    'channel' : fields.String(4096),
    'timing_nature' : fields.String(1024),
    'validity' : fields.String(1024),
    'title' : fields.String,
    'description' : fields.String,
    'sn_title' : fields.String,
    'sn_description' : fields.String,
    'tm_title' : fields.String,
    'tm_description' : fields.String,
    'created_date' : fields.DateTime,
    'updated_date' : fields.DateTime,
}

incident_list_fields = {
    'incidents': fields.List(fields.Nested(incident_fields))
}

@api.resource('/incidents')
class IncidentList(Resource):
    @marshal_with(incident_fields)
    def get(self):
        """List all registered incidents"""
        return get_all_incidents()

    def post(self):
        """Creates a new Incident """
        data = request.get_json()
        return save_new_incident(data=data)


@api.resource('/incidents/<id>')
class Incident(Resource):
    @marshal_with(incident_fields)
    def get(self, id):
        """get a incident given its identifier"""
        incident = get_a_incident(id)
        if not incident:
            api.abort(404)
        else:
            return incident

    def put(self, id):
        """Update a given Incident """
        data = request.get_json()
        return update_a_incident(id=id, data=data)

    def delete(self, id):
        """Delete a given Incident """
        return delete_a_incident(id)