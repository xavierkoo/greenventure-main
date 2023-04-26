<h1 align="center"> GreenVenture </h1> <br>

<p>
GreenVenture is an innovative mobile application that incentivizes users to recycle non-contaminated materials by providing rewards for their efforts. Inspired by the successful Healthy 365 app from the Health Promotion Board (HPB), GreenVenture takes a similar approach, allowing users to scan a QR code to earn points for recycling. This not only motivates users to take action towards a more sustainable future but also provides instant feedback on whether their item is a valid recyclable. By making recycling a more rewarding and engaging experience, GreenVenture aims to encourage a wider community to participate in environmental efforts and make a positive impact on the planet.
</p>

## Table of Contents

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Technical Overview Diagram](#technical-overview-diagram)
- [Database Entity-Relationship Diagram](#database-entity-relationship-diagram)
- [API Documentation](#api-documentation)
- [Requirements](#requirements)
- [Screenshots](#screenshots)

## Tech Stack
* Authentication: OAuth2 with Facebook SSO Login
* Front-End: Vue.js & React.js (The frontend repository can be found [here](https://github.com/xavierkoo/greenventure-frontend).)
* Back-End: Flask & Node.js + Express.js
* Databases: MySQL & MongoDB
* Tools: Docker, LavinMQ & nodemailer

## Features

* Participate and complete recycling themed missions and earn points
* Redeem vouchers with points
* Participate in the community and view the leaderboards

## Technical Overview Diagram
Click the image for the expanded view
<img width="3244" alt="Technical Overview Diagram" src="https://user-images.githubusercontent.com/86020207/234479488-6ad16578-963a-43f6-a59f-b1f8f5f14a58.png">

## Database Entity-Relationship Diagram
![ESD_Project_ER_Diagram drawio](https://user-images.githubusercontent.com/86020207/234415701-63608ae9-94a9-4d96-81ef-23002fba0d34.png)

## API Documentation
[API Docs](https://drive.google.com/drive/folders/1g18KMNGLlNmEHGi0fD0SDVTmqsj8y6BW?usp=share_link)

## Requirements
The frontend of the application can be run locally. The backend can be run in a Docker container. The setup requirements are listed below:

### Frontend
Clone [greenventure-frontend](https://github.com/xavierkoo/greenventure-frontend):
```bash
$ git clone git@github.com:xavierkoo/greenventure-frontend.git
```

Open your terminal in the local project root folder, and execute:
```bash
$ npm install
```

Run the application
```bash
$ npm run dev
```

Application will run by default on port `5173` <br>

### Backend
Clone greenventure-main:
```bash
$ git clone git@github.com:xavierkoo/greenventure-main.git
```

#### Setup Databases
* Run load.sql script to initialize the databases.<br>
* Configure MongoDB connection for Leaderboard Service. Refer to this [README](https://github.com/xavierkoo/greenventure-main/tree/main/server/leaderboards#:~:text=3%20weeks%20ago-,README.md,-greenventure%2Dleaderboards).

#### Run Docker

First build the image:
```bash
$ docker-compose build
```

When ready, run it:
```bash
$ docker-compose up
```
Secondary UIs: <br>
* `recycling-bin-frontend` - `8081`
* `leaderboards` - `3000`

## Screenshots
<p>
  <img src="https://user-images.githubusercontent.com/86020207/234412629-d8078b14-54c5-40dd-b807-0fdd8b822442.png" alt="Screenshot" width="26%">
  <img src="https://user-images.githubusercontent.com/86020207/234413020-e4f9da98-c84a-4e35-bed7-e180b09d876d.png" alt="Screenshot" width="26%">
  <img src="https://user-images.githubusercontent.com/86020207/234413289-4e79121a-e905-41e0-a686-823b8861153e.png" alt="Screenshot" width="25%">
  <img src="https://user-images.githubusercontent.com/86020207/234413363-766f20ec-fc51-4cb7-98c7-353eab447e80.png" alt="Screenshot" width="25%">
  <img src="https://user-images.githubusercontent.com/86020207/234413372-e2bcce41-f747-4896-954b-5be562205e6a.png" alt="Screenshot" width="25%">
</p>
