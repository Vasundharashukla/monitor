# Monitoring Application

This application is the main application that leverages the [health reporter api](https://github.com/vasundharashukla/health-reporter) to get metadata
and metric details about an AWS EC2 instance.

**site-url**: [http://monitoring-env.eba-kmh3ybxg.ap-south-1.elasticbeanstalk.com](http://monitoring-env.eba-kmh3ybxg.ap-south-1.elasticbeanstalk.com)

## Technology Used
- **Programming Languages**
	- Python
	
- **Frameworks**
	- Flask 1.1.1

- **Databases**
	- AWS RDS

## Database Schema

- **user table**: fields(username(varchar primary_key), password(varchar), email(varchar))
- **instance table**: fields(id(integer primary_key), instance_id(varchar), username(varchar foreign_key(user.username)))
- **data table**: fields(id(integer primary_key), instance_id(varchar foreign_key(instance.instance_id)), 
                            metric(varchar), timestamp(varchar), value(float), unit(varchar))
- **params table**: fields(parameter(varchar primary_key), value(integer))

## API Endpoints

- /create-user - Route to create a new user. Accepts a POST request with json data in the given format:
```javascript
{
    "username": '<your-username>',
    "password": '<your-password>',
    "email": '<your-email>'
}
```
- /add-instance - Route to add a new instance to database for a user. Accepts a POST request with json data in the given format:
```javascript
{
    "username": '<your-username>',
    "password": '<your-password>',
    "InstanceId": '<ec2-instance-id>'
}
```

- /get-instances - send a GET request to get instance assigned to the given user. 
```javascript
{
    "username": '<your-username>',
    "password": '<your-password>',
}
```

- /halt - Route to remove instance for a given user. Accepts a post request with json data in the given format:
```javascript
{
    "username": '<your-username>',
    "password": '<your-password>',
    "InstanceId": '<list containing ec2-instance-id>'
}
```

- /api/fork/metrics - Route to call health reporter api to get metric data and store it into db. Accepts a GET request with json data in the given format:
```javascript
{
    "username": '<your-username>',
    "password": '<your-password>',
    "attributes": '<list containing names of metric>' // eg ["CPUUtilization", "NetworkIn"]
}
```
- /api/fork/metadata - Route to call health reporter api to get metric data and store it into db. Accepts a GET request with json data in the given format:
```javascript
{
    "username": '<your-username>',
    "password": '<your-password>',
}
```
- /set/interval - Route to set interval after which the data from api shall be obtained. Accepts a POST request with json data in the given format:
```javascript
{
    "username": '<your-username>',
    "password": '<your-password>',
    "interval": '<integer-value>'
}
```
- /set/threshold - Route to set threshold for metric values. Accepts a POST request with json data in the given format:
```javascript
{
    "username": '<your-username>',
    "password": '<your-password>',
    "threshold": '<integer-value>'
}
```
- /check-threshold - Route to check if any metric value exceeds threshold. All such values are then mailed to the user. Accepts a POST request with json data in the given format:
```javascript
{
    "username": '<your-username>',
    "password": '<your-password>',
}
```
## Credits
- Application created and developed by [Vasundhara Shukla](https://github.com/Vasundharashukla/ "Vasundhara Shukla").
- Contact Email: [17ucc065@lnmiit.ac.in](mailto:17ucc065@lnmiit.ac.in "17ucc065@lnmiit.ac.in")
