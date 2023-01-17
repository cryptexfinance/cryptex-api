
import os, logging, uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.database import db
from api.app1.models.models import CryptKeeper
from werkzeug.utils import secure_filename
from web3 import Web3
from api.app1.utils import validations


UPLOAD_IMAGES_FOLDER = "/usr/src/api/static/images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

_INFURA_KEY = "INFURA_KEY"

class CryptKeeperController:
    """
    Controller class for Crypt Keepers
    """
    def __init__(self, updating):
        self._updating = updating
        provider = Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{os.environ.get(_INFURA_KEY)}")
        self._web3 = Web3(provider)
        self._errors = list()

    def is_data_valid(self, data):
        is_valid = True
        if not self._updating:
            if not self._web3.isChecksumAddress(data["address"]):
                self._errors.append({
                    "field": "address",
                    "message": "The address is invalid."    
                })
                is_valid = False
        
            address = self._web3.ens.address(data["eth_name"])
            if address is None:
                address = data["eth_name"]
                if not self._web3.isChecksumAddress(data["eth_name"]):
                    self._errors.append({
                        "field": "eth_name",
                        "message": "The eth_name is invalid."    
                    })
                    is_valid = False

            if address.lower() != data["address"].lower():
                self._errors.append({
                        "field": "eth_name",
                        "message": "Field address is not equal  to field eth name"    
                    })
                is_valid = False    

        if validations.is_empty(data["name"]) or len(data["name"]) > 30 :
            self._errors.append({
                "field": "name",
                "message": "Name is invalid."    
            })
            is_valid = False

        if validations.is_empty(data["expertise"]) or len(data["expertise"]) > 100:
            self._errors.append({
                "field": "expertise",
                "message": "The expertise field is invalid."    
            })
            is_valid = False

        if validations.is_empty(data["why"]) or len(data["why"]) > 2500:
            self._errors.append({
                "field": "address",
                "message": "The why field is invalid."    
            })
            is_valid = False

        if not validations.is_twitter_name(data["twitter"]) and not validations.is_empty(data["twitter"]):
            self._errors.append({
                "field": "twitter",
                "message": "Not a valid twitter username."
            })
            is_valid = False

        if not validations.is_discord_name(data["discord"]) and not validations.is_empty(data["discord"]):
            self._errors.append({
                "field": "discord",
                "message": "Not a valid discord username"    
            })
            is_valid = False

        return is_valid

    def allowed_file(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_file(self, files, name):
        # check if the post request has the file part
        if files is None:
            if not self._updating:
                self._errors.append({
                    "field": "image",
                    "message": "Image should be provided."
                })
            return ""

        if "file" not in files:
            if not self._updating:
                self._errors.append({
                    "field": "image",
                    "message": "Image should be provided."
                })
            return ""

        file = files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        filename = secure_filename(file.filename)
        if filename == "":
            return ""
        
        if file and self.allowed_file(filename):
            new_name = str(uuid.uuid1())
            extension = filename.rsplit('.', 1)[1].lower()
            file_path = os.path.join(UPLOAD_IMAGES_FOLDER, "{}.{}".format(new_name, extension))
            file.save(file_path)
            return "images/{}.{}".format(new_name, extension)
        else:
            self._errors.append({
                "field": "image",
                "message": "File type is not valid."
            })    

        return ""   

    def create(self, data, files):
        image_path = self.upload_file(files, data["name"])
        if self.is_data_valid(data) and image_path != "":
            try:
                keeper = CryptKeeper(
                            address=data["address"], 
                            name=data["name"],
                            eth_name=data["eth_name"], 
                            expertise=data["expertise"],
                            why=data["why"],
                            image=image_path,
                            discord=data["discord"],
                            twitter=data["twitter"]
                        )
                db.session.add(keeper)
                db.session.commit()

                return dict({
                    "status": "success",
                    "errors": list()
                })
            except IntegrityError as ex:
                logging.error(f"Trying to create Cryp Keeper, address already exists: {ex}")
                self._errors.append({
                    "field": "address",
                    "message": "Cryp Keeper address already exists"
                })
                return dict({
                    "status": "error",
                    "errors": self._errors
                })
            except SQLAlchemyError as ex:
                logging.error(f"Trying to create Cryp Keeper: {ex}")
                self._errors.append({
                    "field": "unknown",
                    "message": "An unkown error has ocurred"
                })
                return dict({
                    "status": "error",
                    "errors": self._errors
                })
        else:
            return dict({
                "status": "error",
                "errors": self._errors
            })

    def update(self, data, files):
        image_path = self.upload_file(files, data["name"])
        if self.is_data_valid(data):
            try:
                keeper = db.session.query(CryptKeeper).get(data.get("keeper_id", 0))
                keeper.name = data["name"]
                keeper.expertise = data["expertise"]
                keeper.why = data["why"]
                keeper.discord = data["discord"]
                keeper.twitter = data["twitter"]
                if image_path != "":
                    keeper.image = image_path
                
                db.session.commit()

                return dict({
                        "status": "success",
                        "errors": list()
                    })
            except SQLAlchemyError as ex:
                logging.error(f"Updating Cryp Keeper: {ex}")
                db.session.close()
                self._errors.append({
                        "field": "unknown",
                        "message": "An unkown error has ocurred"
                    })
                return dict({
                        "status": "error",
                        "errors": list()
                    })
        else:
            return dict({
                        "status": "error",
                        "errors": self._errors
                    })

    def all(self):
        try:
            keepers_list = list()
            keepers = CryptKeeper.query.all()
            for keeper in keepers:
                keepers_list.append(keeper.serialize())
            return keepers_list
        except SQLAlchemyError as ex:  
            logging.error(f"Getting all keepers: {ex}") 
            return list()

    def get_by_address(self):
        pass  
