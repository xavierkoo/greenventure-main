/* Loading the environment variables from the .env file. */
require('dotenv').config();

// environment variables for port and mongodb
const PORT = process.env.PORT;

const MONGODB_URI = process.env.NODE_ENV === 'test'
    ? process.env.TEST_MONGODB_URI
    : process.env.MONGODB_URI;

module.exports = {
    MONGODB_URI,
    PORT,
};
