// imports application and http to run server
const http = require('http');
const app = require('./app');
const config = require('./utils/config');
const logger = require('./utils/logger');

// create http server
const server = http.createServer(app);

// use info to log
server.listen(config.PORT, () => {
    logger.info(`Server running on port ${config.PORT}`);
});
