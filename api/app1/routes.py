from flask import Blueprint, jsonify, request
from flask_cors import CORS
from api.app1.controllers.crypt_keeper import CryptKeeperController

app1_blueprint = Blueprint('app1', __name__)
CORS(app1_blueprint)

@app1_blueprint.route("/cryptkeeper/create", methods=["POST"])
def create_cryptkeeper():    
    keeper = CryptKeeperController(False)
    reponse = keeper.create(request.form, request.files)
    return reponse

@app1_blueprint.route("/cryptkeeper/update", methods=["POST"])
def update_cryptkeeper():    
    keeper = CryptKeeperController(True)
    reponse = keeper.update(request.form, request.files)
    return reponse    

@app1_blueprint.route("/cryptkeeper/all", methods=["GET"])
def all_cryptkeeper():    
    keeper = CryptKeeperController(False)
    reponse = keeper.all()
    return jsonify(reponse)