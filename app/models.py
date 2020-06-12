from app import db

class User(db.Model):
    __tablename__='user'
    username = db.Column(db.String(64), index=True, primary_key=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    instances = db.relationship('Instance', cascade="all,delete", backref="user")

class Instance(db.Model):
    __tablename__='instance'
    id=db.Column(db.Integer, index=True, primary_key=True)
    instance_id = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), db.ForeignKey('user.username'))
    metrics = db.relationship('Data', cascade="all,delete", backref="instance")

class Data(db.Model):
    __tablename__='data'
    id=db.Column(db.Integer, index=True, primary_key=True)
    instance_id = db.Column(db.String(64), db.ForeignKey('instance.instance_id'))
    metric = db.Column(db.String(128))
    timestamp = db.Column(db.String(128))
    value = db.Column(db.Float(precision=4))
    unit=db.Column(db.String(10))

class Params(db.Model):
    __tablename__='params'
    parameter = db.Column(db.String(64), index=True, primary_key=True)
    value = db.Column(db.Integer)
