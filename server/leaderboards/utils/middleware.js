const logger = require('./logger');

// logger middleware
const requestLogger = (request, response, next) => {
    logger.info('Method:', request.method);
    logger.info('Path:  ', request.path);
    logger.info('Body:  ', request.body);
    logger.info('---');
    next();
};

// unknown endpoint respond with error code 404
const unknownEndpoint = (request, response) => {
    response.status(404).send({ error: 'unknown endpoint' });
};

module.exports = {
    requestLogger,
    unknownEndpoint,
};
