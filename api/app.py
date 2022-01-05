from flask import Flask
from database import db
from web3_app.routes import web3_blueprint
from app1.routes import app1_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(web3_blueprint)
    app.register_blueprint(app1_blueprint)    

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://cryptex:123456@db:5432/cryptex"
    db.init_app(app)
    #Migrate(app, db)

    return app

new_app = create_app()