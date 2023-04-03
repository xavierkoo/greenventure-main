# greenventure-notifications
docker build -t notification .                                                    

docker run -d --name notification notification

# Documentation
LavinMQ - cloud AMQP <br>
nodemailer

#### Publish messages to:
```
connectionUrl = <LavinMQ URL>
queueName = 'notifications'
```

# Payload
JSON Object:
```
{
  "email": RECEIVER_EMAIL_ADDRESS,
  "subject": EMAIL_SUBJECT,
  "message": EMAIL_MESSAGE
}
```
