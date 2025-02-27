from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from .auth import require_auth

app = Flask(__name__)
api = Api(app)

class DataResource(Resource):
    @require_auth
    def get(self):
        """
        Point de terminaison REST pour récupérer les données
        """
        try:
            # Logique de récupération des données
            return jsonify({"status": "success", "data": data})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

api.add_resource(DataResource, '/api/v1/data') 