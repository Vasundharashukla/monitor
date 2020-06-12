import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'_5#y2L"F4Q8z\n\xec]/'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<pass>@<db-endpoint>/<db-name>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_URL = "http://healthrepapi-env.eba-rgbprbna.ap-south-1.elasticbeanstalk.com/fork"
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT= 465
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True
    MAIL_USERNAME= '<email-id>'
    MAIL_PASSWORD= '<email-pass>'
    MAIL_DEFAULT_SENDER= 'tester'

