import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'_5#y2L"F4Q8z\n\xec]/'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin123@database-2.ck1rk0z9fjpp.ap-south-1.rds.amazonaws.com/monitor'#os.environ.get('DATABASE_URL') or \
        #'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_URL = "http://healthrepapi-env.eba-rgbprbna.ap-south-1.elasticbeanstalk.com/fork"
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT= 465
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True
    MAIL_USERNAME= 'vasundharashukla799@gmail.com'
    MAIL_PASSWORD= 'V@su7998'
    MAIL_DEFAULT_SENDER= 'tester'

