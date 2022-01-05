from api.database import db

class CryptKeeper(db.Model):
    __tablename__ = 'crypt_keeper'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(25))
    eth_name = db.Column(db.String(128))
    expertise = db.Column(db.String(120))
    why = db.Column(db.String(4000))
    image = db.Column(db.String(255))
    discord = db.Column(db.String(30))
    twitter = db.Column(db.String(30))

    def __init__(self, address, name, eth_name, expertise, why,  image, discord, twitter):
        self.address = address
        self.name = name
        self.eth_name = eth_name
        self.expertise = expertise
        self.why = why 
        self.image = image
        self.discord = discord
        self.twitter = twitter

    def serialize(self):
        return {"id": self.id,
                "address": self.address,
                "name": self.name,
                "eth_name": self.eth_name,
                "expertise": self.expertise,
                "why": self.why,
                "image": self.image,
                "discord": self.discord,
                "twitter": self.twitter
            }

    def __repr__(self):
        return f"<CryptKeeper {self.eth_name}>"