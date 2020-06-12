from app import app, db, mail
from flask import request, jsonify
from .models import User, Instance, Params, Data
from pprint import pprint
from flask_mail import Message
import requests, warnings
warnings.filterwarnings('ignore')

## MONITORING FEATURES
@app.route('/create-user', methods=["POST"])
def createUser():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    email = req.get('email', None)
    if password == None or username == None or email == None:
        return jsonify({"result": "Invalid request"})
        
    check = User.query.get(username)

    if check is not None:
        return jsonify({'result': 'username already exists'})
    
    try:
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({'result': 'user created successfully'})
    except Exception as e:
        print(e)
        return jsonify({"result": "error occured"})

@app.route('/add-instances', methods=["POST"])
def addInstance():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    instance = req.get('InstanceId', "")
    
    if not username or not password:
        return jsonify({"result": "Authentication Failed"})
    
    f = User.query.get(username)

    if not f:
        return jsonify({"result": "user not found"})
    
    if f.password != password:
        return jsonify({"result": "wrong password"})
    
    if instance == "":
        return jsonify({"result": "Add an instance id"})

    try:
        resp = dict()
        check = Instance.query.filter((Instance.instance_id==instance) & (Instance.username==username)).first()
        print(check)
        if check is None:
            ins = Instance(username=username, instance_id=instance)
            db.session.add(ins)
            db.session.commit()
            resp[instance] = 'added successfully'
        else:
            resp[instance] = 'already exists'
        return jsonify({"result": resp})

    except Exception as e:
        print(e)
        return jsonify({"result": "error occured"})

@app.route('/get-instances', methods=["GET"])
def getInstance():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    if not username or not password:
        return jsonify({"result": "Authentication Failed"})
    
    f = User.query.get(username)

    if not f:
        return jsonify({"result": "user not found"})
    
    if f.password != password:
        return jsonify({"result": "wrong password"})

    try:
        instances = Instance.query.filter((Instance.username == username)).all()
        result = [instance.instance_id for instance in instances]
        return jsonify({"result": {"Instances": result}})
    except Exception as e:
        print(e)
        return jsonify({"result": "error occured"})

@app.route('/get-data', methods=["GET"])
def getData():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    if not username or not password:
        return jsonify({"result": "Authentication Failed"})
    
    f = User.query.get(username)

    if not f:
        return jsonify({"result": "user not found"})
    
    if f.password != password:
        return jsonify({"result": "wrong password"})

    try:
        data = Data.query.join(Instance).filter_by(username=username).all()
        resp = list()
        for ins in data:
            resp.append({'instance_id': ins.instance_id,
                         'metric': ins.metric,
                         'value': ins.value,
                         'timestamp': ins.timestamp,
                         'unit': ins.unit})
        return jsonify({"result": resp})
    except Exception as e:
        print(e)
        return jsonify({"result": "error occured"})

@app.route('/halt', methods=["POST"])
def haltMonitoring():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    listOfInstanceIds = req.get('InstanceId', [])
    
    if not username or not password:
        return jsonify({"result": "Authentication Failed"})
    
    f = User.query.get(username)

    if not f:
        return jsonify({"result": "user not found"})
    
    if f.password != password:
        return jsonify({"result": "wrong password"})
    
    if listOfInstanceIds == []:
        return jsonify({"result": "Add atleast one instance id"})

    try:
        instances = Instance.query.filter(Instance.instance_id.in_(listOfInstanceIds)).delete(False)
        db.session.commit()
        return jsonify({"result": "deletion successful!"})
    except Exception as e:
        print(e)
        return jsonify({"result": "error occured"})

@app.route('/set/<value>', methods=["POST"])
def setParam(value):
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)

    if not username or not password:
        return jsonify({"result": "Authentication Failed"})
    
    f = User.query.get(username)

    if not f:
        return jsonify({"result": "user not found"})
    
    if f.password != password:
        return jsonify({"result": "wrong password"})

    if value not in {"threshold", "interval"}:
        return jsonify({"result": "invalid parameter"})
    
    try:
        set_as = req.get(value, None)
        if set_as is None:
            return jsonify({"result": f"{value} value not found"})
        else:
            check = Params.query.filter(Params.parameter==value).first()
            if check is not None:
                check.value = set_as
                db.session.commit()
            else:
                new = Params(parameter=value, value=set_as)
                db.session.add(new)
                db.session.commit()
            return jsonify({"result": "OK"})
    except Exception as e:
        print(e)
        return jsonify({"result": "error occured"})

## API CALLS    
@app.route('/api/fork/<value>', methods=["GET"])
def APICalls(value):
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    
    if not username or not password:
        return jsonify({"result": "Authentication Failed"})
    
    f = User.query.get(username)

    if not f:
        return jsonify({"result": "user not found"})
    
    if f.password != password:
        return jsonify({"result": "wrong password"})

    try:
        api_url = app.config.get("API_URL", "")
        if value == "metrics":
            instances = Instance.query.filter((Instance.username == username)).all()
            instances = [instance.instance_id for instance in instances]
            inter = Params.query.filter(Params.parameter=="interval").first()
            if inter is None:
                inter=2
            else:
                inter=inter.value
            print(inter)
            api_req = {"dimensions": [], "interval": req.get("interval", 2), "attributes": req.get("attributes", [])}
            
            if instances==[]:
                return jsonify({"result": "No instances inside database"})
            if api_req["attributes"] == []:
                return jsonify({"result": "Invalid Request"})
                
            for ins in instances:
                api_req["dimensions"].append({"Name": "InstanceId", "Value": ins})
            
            api_res = requests.get(f'{api_url}/{value}', json = api_req)
            api_res = api_res.json()["result"]
            data = list()
            for attr in api_req.get("attributes"):
                t = dict()
                for d in api_res[attr]["Datapoints"]:
                    t["instance_id"] = Instance.query.filter(Instance.username==username).first().instance_id
                    t["metric"] = attr
                    t["value"] = d["Maximum"]
                    t["timestamp"] = d["Timestamp"]
                    t["unit"] = d["Unit"]
                    data.append(t)
                    add = Data(instance_id=t["instance_id"],
                               metric=t["metric"],
                               value=round(t["value"], 4),
                               timestamp=t["timestamp"],
                               unit=t["unit"])
                    db.session.add(add)
            db.session.commit()
            pprint(api_res)
            return jsonify({"result": data})
        if value == "metadata":
            api_res = requests.get(f'{api_url}/{value}')
            return api_res.json()

    except Exception as e:
        print(e)
        return jsonify({"result": "error occured"})

@app.route('/check-threshold', methods=["POST"])
def checkThreshold():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    
    if not username or not password:
        return jsonify({"result": "Authentication Failed"})
    
    f = User.query.get(username)

    if not f:
        return jsonify({"result": "user not found"})
    
    if f.password != password:
        return jsonify({"result": "wrong password"})

    try:
        threshold = Params.query.filter(Params.parameter=="threshold").first()
        threshold = threshold.value

        data = Data.query.join(Instance).filter_by(username=username).all()
        lis = list()
        for ins in data:
            if ins.value > threshold:
                lis.append(f'{ins.metric}, {ins.timestamp}: {ins.value} {ins.unit}')
        if len(lis)>=1:
            with app.app_context():
                body = "Limit exceeded for the following metric:\n" + "\n".join(lis)
                msg = Message(subject="Threshold Exceeded",
                              sender=app.config.get("MAIL_DEFAULT_SENDER"), #app.config.get("MAIL_USERNAME"),
                              recipients=[User.query.get(username).email], # replace with your email for testing
                              body=body)
                mail.send(msg)
        return jsonify({"result": "OK"})
    except Exception as e:
        print(e)
        return jsonify({"result": "error occured"})
    

            
