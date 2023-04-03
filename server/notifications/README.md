# greenventure-notifications
docker build -t notification .                                                    

docker run -d --name notification notification

# Documentation
LavinMQ - cloud AMQP <br>
nodemailer

#### Publish messages to:
```
connectionUrl = 'amqps://pjfowojn:hi7ZiPRdS6bEQDHZo-_CKeLH7vbINRCn@possum.lmq.cloudamqp.com/pjfowojn'
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
