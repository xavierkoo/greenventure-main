/* This is the leaderboards router. It handles the updating and retrieving of leaderboards. */
const Leaderboard = require('../models/leaderboard')
const leaderboardsRouter = require('express').Router()

/* This is a GET request to the users endpoint. It is retrieving the users from the
database. */
leaderboardsRouter.get('/', async (request, response) => {
    const users = await Leaderboard
        .find({})
    if (users) {
        response.json(users)
    } else {
        response.status(404).end()
    }
});

/* This is a GET request to the users endpoint. It is retrieving the users from the
database. */
leaderboardsRouter.get('/:userId', async (request, response) => {
    const user = await Leaderboard.findOne({ userId: request.params.userId });
    if (user) {
      response.json(user);
    } else {
      response.status(404).end();
    }
});

/* This is a POST request to the users endpoint. It is creating a new user in the database. */
leaderboardsRouter.post('/', async (request, response, next) => {
    const { body } = request

    const user = new Leaderboard({
        userId: body.userId,
        name: body.name,
        points: body.points,
    })

    try {
        const savedUser = await user.save()
        response.status(201).json(savedUser)
    } catch (exception) {
        next(exception)
    }
});

/* This is a PATCH request to the users endpoint. It is updating a user in the database. */
leaderboardsRouter.patch('/:userId', async (request, response, next) => {
    const { body } = request;
  
    try {
        const userToUpdate = await Leaderboard.findOne({ userId: request.params.userId });
        const updatedPoints = userToUpdate.points + body.points;
        const updatedUser = await Leaderboard.findOneAndUpdate({ userId: request.params.userId }, { points: updatedPoints }, { new: true });
        response.status(204).json(updatedUser);
    } catch (exception) {
        next(exception);
    }
});

module.exports = leaderboardsRouter