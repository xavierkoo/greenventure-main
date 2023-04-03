/* This is the main file for the backend. It is importing all the required modules and routers.
It is also connecting to the mongodb database. */
const express = require('express');
const cors = require('cors');
const app = express();
const mongoose = require('mongoose');
const config = require('./utils/config');
const middleware = require('./utils/middleware');
const logger = require('./utils/logger');
require('express-async-errors');

mongoose.set('strictQuery', false)

const leaderboardsRouter = require('./controllers/leaderboards');

// connect to mongodb database
logger.info('connecting to', config.MONGODB_URI);

mongoose.connect(config.MONGODB_URI)
    .then(() => {
        logger.info('connected to MongoDB');
    })
    .catch((error) => {
        logger.error('error connecting to MongoDB:', error.message);
    });

// execute express middleware functions
app.use(cors());
app.use(express.static('build'));
app.use(express.json());
app.use(middleware.requestLogger);

app.use('/api/leaderboards', leaderboardsRouter);

// error handler and unknown endpoint must be after routers
app.use(middleware.unknownEndpoint);

module.exports = app;