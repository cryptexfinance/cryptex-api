
import os, logging, uuid
from web3 import Web3
from django.db import DatabaseError
from werkzeug.utils import secure_filename
from PIL import Image
from django.conf import settings
from .models import CryptKeeper
from . import validations


UPLOAD_IMAGES_FOLDER = settings.MEDIA_ROOT
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

_INFURA_KEY = "INFURA_KEY"

logger = logging.getLogger('sales.custom')

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

            if is_valid:
                try:
                    CryptKeeper.objects.get(address=data["address"])
                    self._errors.append({
                        "field": "address",
                        "message": "Crypt. Keeper address already exists"
                    })
                    is_valid = False
                except  CryptKeeper.DoesNotExist:
                    pass     

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

    def upload_file(self, files):
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
        try:
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            filename = secure_filename(file.name)
            if filename == "":
                return ""
            
            keeper_image = Image.open(file)
            if file and self.allowed_file(filename):
                new_name = str(uuid.uuid1())
                extension = filename.rsplit('.', 1)[1].lower()
                file_path = os.path.join(UPLOAD_IMAGES_FOLDER, "{}.{}".format(new_name, extension))
                
                keeper_image.save(file_path, extension)
                return "images/{}.{}".format(new_name, extension)
            else:
                self._errors.append({
                    "field": "image",
                    "message": "File type is not valid."
                })
        except Exception as ex:
            logger.error(f"Error saving image: {ex}")
            self._errors.append({
                "field": "image",
                "message": f"An error occurred trying to save the image: {ex}"
            })

        return ""

    def create(self, data, files):
        image_path = self.upload_file(files)
        if self.is_data_valid(data):
            try:
                CryptKeeper.objects.create(
                    address = data["address"], 
                    name = data["name"],
                    eth_name = data["eth_name"], 
                    expertise = data["expertise"],
                    why = data["why"],
                    image = image_path,
                    discord = data["discord"],
                    twitter = data["twitter"]
                )

                return dict({
                    "status": "success",
                    "errors": list()
                })
            except DatabaseError as ex:
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
        image_path = self.upload_file(files)
        if self.is_data_valid(data):
            try:
                keeper = CryptKeeper.objects.get(pk = data.get("keeper_id", 0))
                keeper.name = data["name"]
                keeper.expertise = data["expertise"]
                keeper.why = data["why"]
                keeper.discord = data["discord"]
                keeper.twitter = data["twitter"]
                if image_path != "":
                    keeper.image = image_path

                keeper.save()    
                return dict({
                        "status": "success",
                        "errors": self._errors
                    })
            except CryptKeeper.DoesNotExist:
                logger.error(f"Crypt. keeper does not exists: {data}")
                self._errors.append({
                        "field": "unknown",
                        "message": "Crypt. keeper does not exists."
                    })
                return dict({
                        "status": "error",
                        "errors": list()
                    })          
            except DatabaseError as ex:
                logger.error(f"Updating Cryp Keeper Database error: {ex}")
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
            keepers = CryptKeeper.objects.all()            
            return keepers
        except DatabaseError as ex:  
            logging.error(f"Getting all keepers: {ex}") 
            return list()
