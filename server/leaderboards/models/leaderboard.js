/* This is the user model. It defines the structure of the user object. */
const mongoose = require('mongoose')
const uniqueValidator = require('mongoose-unique-validator')

const leaderboardSchema = new mongoose.Schema({
    userId : {
        type: String,
        required: true,
    },
    name: {
        type: String,
        required: true,
    },
    points: {
        type: Number,
        required: true,
        default: 0,
    },
})

leaderboardSchema.set('toJSON', {
    transform: (document, returnedObject) => {
        returnedObject.id = returnedObject._id.toString()
        delete returnedObject._id
        delete returnedObject.__v
    }
})

module.exports = mongoose.model('Leaderboard', leaderboardSchema)
