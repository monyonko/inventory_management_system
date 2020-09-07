
class Config():
    DEBUG = True
    SECRET_KEY = "9960b9b6ca2ea49ec7ef6f133b382a9b"

class  Development(Config):
    # database://user:password@host:port/databasename
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:borauhai@127.0.0.1:5432/inventory_management_system'

class Production():
    pass


