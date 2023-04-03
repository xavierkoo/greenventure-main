const amqp = require('amqplib');
const nodemailer = require('nodemailer');

const connectionUrl = 'amqps://pjfowojn:hi7ZiPRdS6bEQDHZo-_CKeLH7vbINRCn@possum.lmq.cloudamqp.com/pjfowojn';
const queueName = 'notifications';

async function connect() {
    try {
        /* This is the code that connects to the AMQP server and creates a channel to listen for
        messages on the queue. */
        const connection = await amqp.connect(connectionUrl);
        console.log('Connected to AMQP server');
        const channel = await connection.createChannel();
        await channel.assertQueue(queueName);
        console.log(`Listening for messages on ${queueName}...`);
        /* This is the code that connects to the AMQP server and creates a channel to listen for
                messages on the queue. */
        channel.consume(queueName, (message) => {
            if (message !== null) {
                try {
                    const content = JSON.parse(message.content.toString());
                    console.log('Received message:', content);
        
                    // Send email notification using Nodemailer
                    const transporter = nodemailer.createTransport({
                        service: 'gmail',
                        auth: {
                            user: 'ogobogobob@gmail.com', // replace with your email
                            pass: 'asjpljcbvljhwghi' // replace with your email password
                        }
                    });
        
                    const mailOptions = {
                        from: 'ogobogobob@gmail.com', // replace with your email
                        to: `${content.email}`,
                        subject: `${content.subject}`,
                        text: `${content.message}`
                    };
        
                    transporter.sendMail(mailOptions, (error, info) => {
                        if (error) {
                            console.error('Error sending email:', error);
                        } else {
                            console.log('Email sent:', info.response);
                        }
                    });
        
                    channel.ack(message);
                } catch (error) {
                    console.error('Error processing message:', error);
                    channel.nack(message, false, false);
                }
            }
        });
    } catch (error) {
        console.error('Error connecting to AMQP server:', error);
    }
}

connect();
