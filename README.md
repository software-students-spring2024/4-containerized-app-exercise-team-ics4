![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# About

This containerized app takes real-time audio feed from users and classifies the it into categories. It then shows metadata about what it believes the sounds to be, and the confidence level for each category.

# Instructions

To run this project, build the docker containers using docker-compose. Pre-requisite is to have docker installed on your system. In the root directory, run:

- `docker-compose up --build`

# Testing Instructions _IMPORTANT_

To test this project, we wanted to isolate the mongo testing environment with the production environment. Therefore, before running `pytest tests/` in the root directories of [machine-learning-client](./machine-learning-client/) and [web-app](./web-app/), make sure to temporarily change the Mongo connection uri string to `mongodb://localhost:27017/` in the respective `app.py` files. Be sure to change them back after testing.

To run tests,

- install dependencies listed in the requirements.txt file
- navigate to [machine-learning-client](./machine-learning-client/) or [web-app](./web-app/) and run `pytest tests/`

# References

[Github Blog on Implementing OpenCV and Live Video Feed](https://github.com/google/mediapipe/issues/4448)

[Used example code from MediaPipe](https://codepen.io/mediapipe-preview/pen/wvxYYmy)

# Team Members

- [Eric Lin](https://github.com/exl7954)
- [Alice Ding](https://github.com/ayd2134)
- [Justin Zhao](https://github.com/zhaojustin)
