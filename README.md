<h1 align="center"> GreenVenture </h1> <br>

<p>
Inspired by the Healthy 365 app launched by the Health Promotion Board (HPB), GreenVenture is an application that rewards users for recyling a non-contaminated recyclable. Like the Healthy 365 app where users are allowed to scan a QRCode to gain points after purchasing a healthier choice product, this approach towards recycling not only incentives users to come ahead to recycle, but also provide instant feedback to users on whether their item is valid recyclable. 
</p>

## Table of Contents

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Requirements](#requirements)

## Tech Stack
* Authentication: OAuth2 with Facebook SSO Login
* Front-End: Vue.js & React.js (https://github.com/GreenVenture/greenventure-frontend)
* Back-End: Flask & Node.js + Express.js
* Databases: MySQL & MongoDB
* Tools: Docker, LavinMQ & nodemailer

## Features

* Participate and complete recycling themed missions and earn points
* Redeem vouchers with points
* Participate in the community and view the leaderboards


## Requirements
The frontend of the application can be run locally or by using the deployed Netlify link. The backend can be run in a docker container, the requirements for the setup is listed below.

### Local - Frontend
Clone greenventure-frontend:
```bash
$ git clone git@github.com:GreenVenture/greenventure-frontend.git
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
Run load.sql script to initialize the database

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
